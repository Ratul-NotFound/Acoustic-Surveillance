import os
import glob
import shutil
import subprocess
import librosa
import soundfile as sf
import numpy as np
import random

ffmpeg_dir = r"C:\Users\mhrat\AppData\Local\ffmpegio\ffmpeg-downloader\ffmpeg\bin"
os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")

DATASET_DIR = "E:/software/acoustic-surveillance/data_prep/q1_dataset/tree_falling"
TEMP_YOUTUBE_DIR = "E:/software/acoustic-surveillance/data_prep/temp_tree_youtube"
ENV_DIR = "E:/software/acoustic-surveillance/data_prep/q1_dataset/00_forest_natural_environment_sound"

# Ensure clean slate
print("Clearing old noisy tree falling dataset...")
if os.path.exists(DATASET_DIR):
    shutil.rmtree(DATASET_DIR)
os.makedirs(DATASET_DIR, exist_ok=True)

if os.path.exists(TEMP_YOUTUBE_DIR):
    shutil.rmtree(TEMP_YOUTUBE_DIR)
os.makedirs(TEMP_YOUTUBE_DIR, exist_ok=True)

VIDEO_URLS = [
    "https://www.youtube.com/watch?v=QDGyPGLGQNw",
    "https://www.youtube.com/watch?v=hExOFTpTLLI",
    "https://www.youtube.com/watch?v=sLifNslAkWI"
]

def load_random_env(duration=1.0, sr=16000):
    files = glob.glob(os.path.join(ENV_DIR, "*.wav"))
    if not files:
        return np.zeros(int(duration * sr))
    
    file = random.choice(files)
    y, _ = librosa.load(file, sr=sr, mono=True)
    
    length = int(duration * sr)
    if len(y) > length:
        start = random.randint(0, len(y) - length)
        y = y[start:start+length]
    else:
        y = np.pad(y, (0, length - len(y)))
    return y

def download_audio():
    print("Downloading pristine tree crashing clips from YouTube...")
    for url in VIDEO_URLS:
        cmd = [
            "python", "-m", "yt_dlp",
            "--extract-audio",
            "--audio-format", "wav",
            "--ffmpeg-location", ffmpeg_dir,
            "--output", os.path.join(TEMP_YOUTUBE_DIR, "%(id)s.%(ext)s"),
            url
        ]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
        except Exception as e:
            print(f"Error downloading {url}: {e}")

def augment_and_save(segment, sr, count):
    # We will generate 3-4 augmented versions of this 1s chunk
    
    # 1. Base (mixed with random ambient forest)
    env = load_random_env(sr=sr)
    base = segment + env * random.uniform(0.1, 0.4)
    out_path = os.path.join(DATASET_DIR, f"real_tree_{count:04d}.wav")
    sf.write(out_path, base, sr)
    count += 1
    
    # 2. Pitch shift down (bigger, heavier tree)
    y_shift_down = librosa.effects.pitch_shift(segment, sr=sr, n_steps=random.uniform(-4, -1))
    env2 = load_random_env(sr=sr)
    shifted_down = y_shift_down + env2 * random.uniform(0.1, 0.4)
    out_path = os.path.join(DATASET_DIR, f"real_tree_{count:04d}.wav")
    sf.write(out_path, shifted_down, sr)
    count += 1
    
    # 3. Pitch shift up (smaller tree / branches snapping)
    y_shift_up = librosa.effects.pitch_shift(segment, sr=sr, n_steps=random.uniform(1, 3))
    env3 = load_random_env(sr=sr)
    shifted_up = y_shift_up + env3 * random.uniform(0.1, 0.4)
    out_path = os.path.join(DATASET_DIR, f"real_tree_{count:04d}.wav")
    sf.write(out_path, shifted_up, sr)
    count += 1
    
    # 4. Time stretch (slower fall)
    y_slow = librosa.effects.time_stretch(segment, rate=random.uniform(0.8, 0.95))
    if len(y_slow) < len(segment):
        y_slow = np.pad(y_slow, (0, len(segment) - len(y_slow)))
    else:
        y_slow = y_slow[:len(segment)]
    env4 = load_random_env(sr=sr)
    stretched = y_slow + env4 * random.uniform(0.1, 0.4)
    out_path = os.path.join(DATASET_DIR, f"real_tree_{count:04d}.wav")
    sf.write(out_path, stretched, sr)
    count += 1
    
    return count

def process_audio():
    print("Extracting and augmenting tree chunks...")
    wav_files = glob.glob(os.path.join(TEMP_YOUTUBE_DIR, "*.wav"))
    
    count = 0
    chunk_length = 1.0 # 1 second
    
    for wav_file in wav_files:
        print(f"Processing {os.path.basename(wav_file)}...")
        try:
            # Load with librosa, mono, 16kHz
            y, sr = librosa.load(wav_file, sr=16000, mono=True)
            
            # Since these are short clips, we take 1s chunks with large overlap
            step = int(0.2 * sr)
            chunk_samples = int(chunk_length * sr)
            
            # If the audio is shorter than 1s, pad it
            if len(y) < chunk_samples:
                y = np.pad(y, (0, chunk_samples - len(y)))
                
            for start_sample in range(0, len(y) - chunk_samples + 1, step):
                segment = y[start_sample:start_sample + chunk_samples]
                
                # Check for silence or low energy (must have snapping/crashing)
                rms = librosa.feature.rms(y=segment)[0]
                if np.max(rms) > 0.05: # threshold for loud cracking/impact
                    count = augment_and_save(segment, sr, count)
                    
                    if count >= 150:
                        print(f"Successfully generated {count} pristine augmented samples.")
                        return
                        
        except Exception as e:
            print(f"Failed to process {wav_file}: {e}")
            
    print(f"Total extracted clips: {count}")

if __name__ == "__main__":
    download_audio()
    process_audio()
    print(f"Finished building dataset in {DATASET_DIR}")
    
    # Clean up temp files
    if os.path.exists(TEMP_YOUTUBE_DIR):
        shutil.rmtree(TEMP_YOUTUBE_DIR)

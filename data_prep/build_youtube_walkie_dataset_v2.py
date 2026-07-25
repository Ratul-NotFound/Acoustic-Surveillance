import os
import glob
import shutil
import subprocess
import librosa
import soundfile as sf
import numpy as np

ffmpeg_dir = r"C:\Users\mhrat\AppData\Local\ffmpegio\ffmpeg-downloader\ffmpeg\bin"
os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")

DATASET_DIR = "E:/software/acoustic-surveillance/data_prep/q1_dataset/walkie_talkie"
TEMP_YOUTUBE_DIR = "E:/software/acoustic-surveillance/data_prep/temp_walkie_youtube_v2"

# Ensure clean slate
print("Clearing old noisy walkie talkie dataset...")
if os.path.exists(DATASET_DIR):
    shutil.rmtree(DATASET_DIR)
os.makedirs(DATASET_DIR, exist_ok=True)

if os.path.exists(TEMP_YOUTUBE_DIR):
    shutil.rmtree(TEMP_YOUTUBE_DIR)
os.makedirs(TEMP_YOUTUBE_DIR, exist_ok=True)

# Explicit video IDs for very short, pure walkie talkie sounds
VIDEO_URLS = [
    "https://www.youtube.com/watch?v=P9mc-TXP4qs",
    "https://www.youtube.com/watch?v=gut8Le1qw9k",
    "https://www.youtube.com/watch?v=_ayjGkfO50Y",
    "https://www.youtube.com/watch?v=6xlrbeVqk-A",
    "https://www.youtube.com/watch?v=3as-riv9jZo",
    "https://www.youtube.com/watch?v=_T2N3bzgn5Q"
]

def download_audio():
    print("Downloading pristine short walkie talkie clips from YouTube...")
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
    # Base save
    out_path = os.path.join(DATASET_DIR, f"real_walkie_{count:04d}.wav")
    sf.write(out_path, segment, sr)
    count += 1
    
    # Pitch shift up
    y_shift_up = librosa.effects.pitch_shift(segment, sr=sr, n_steps=2)
    out_path = os.path.join(DATASET_DIR, f"real_walkie_{count:04d}.wav")
    sf.write(out_path, y_shift_up, sr)
    count += 1
    
    # Pitch shift down
    y_shift_down = librosa.effects.pitch_shift(segment, sr=sr, n_steps=-2)
    out_path = os.path.join(DATASET_DIR, f"real_walkie_{count:04d}.wav")
    sf.write(out_path, y_shift_down, sr)
    count += 1
    
    # Time stretch (fast)
    y_fast = librosa.effects.time_stretch(segment, rate=1.2)
    if len(y_fast) < len(segment):
        y_fast = np.pad(y_fast, (0, len(segment) - len(y_fast)))
    else:
        y_fast = y_fast[:len(segment)]
    out_path = os.path.join(DATASET_DIR, f"real_walkie_{count:04d}.wav")
    sf.write(out_path, y_fast, sr)
    count += 1
    
    return count

def process_audio():
    print("Extracting and augmenting walkie talkie chunks...")
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
                
                # Check for silence
                rms = librosa.feature.rms(y=segment)[0]
                if np.mean(rms) > 0.01: # Must have audible sound
                    count = augment_and_save(segment, sr, count)
                    
                    if count >= 300:
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

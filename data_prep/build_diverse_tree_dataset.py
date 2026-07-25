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
TEMP_YOUTUBE_DIR = "E:/software/acoustic-surveillance/data_prep/temp_tree_compilation"
ENV_DIR = "E:/software/acoustic-surveillance/data_prep/q1_dataset/00_forest_natural_environment_sound"

# Ensure clean slate
print("Clearing old dataset...")
if os.path.exists(DATASET_DIR):
    shutil.rmtree(DATASET_DIR)
os.makedirs(DATASET_DIR, exist_ok=True)

if os.path.exists(TEMP_YOUTUBE_DIR):
    shutil.rmtree(TEMP_YOUTUBE_DIR)
os.makedirs(TEMP_YOUTUBE_DIR, exist_ok=True)

# 6 minute compilation of tree falls
VIDEO_URLS = [
    "https://www.youtube.com/watch?v=mto27Oi1hM0", # Tree Falling Compilation
    "https://www.youtube.com/watch?v=ZkFsdlAdoEE"  # Tree felling post-wildfire
]

def load_random_env(duration=1.5, sr=16000):
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
    print("Downloading pristine tree crashing compilations from YouTube...")
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

def process_audio():
    print("Extracting diverse tree falls from compilations...")
    wav_files = glob.glob(os.path.join(TEMP_YOUTUBE_DIR, "*.wav"))
    
    count = 0
    chunk_length = 1.5 # 1.5 seconds per crash
    
    for wav_file in wav_files:
        print(f"Scanning compilation {os.path.basename(wav_file)}...")
        try:
            # Load with librosa, mono, 16kHz
            y, sr = librosa.load(wav_file, sr=16000, mono=True)
            
            chunk_samples = int(chunk_length * sr)
            
            start_sample = 0
            while start_sample < len(y) - chunk_samples:
                segment = y[start_sample:start_sample + chunk_samples]
                
                # Check for massive volume spike (crash)
                rms = librosa.feature.rms(y=segment)[0]
                if np.max(rms) > 0.08: # high threshold for loud cracking/impact
                    # We found a crash! 
                    
                    # 1. Base crash
                    env1 = load_random_env(duration=chunk_length, sr=sr)
                    mixed1 = segment + env1 * random.uniform(0.1, 0.4)
                    sf.write(os.path.join(DATASET_DIR, f"real_tree_{count:04d}.wav"), mixed1, sr)
                    count += 1
                    
                    # 2. Pitch shifted slightly for robustness
                    y_shift = librosa.effects.pitch_shift(segment, sr=sr, n_steps=random.uniform(-3, 3))
                    env2 = load_random_env(duration=chunk_length, sr=sr)
                    mixed2 = y_shift + env2 * random.uniform(0.1, 0.4)
                    sf.write(os.path.join(DATASET_DIR, f"real_tree_{count:04d}.wav"), mixed2, sr)
                    count += 1
                    
                    print(f"Extracted unique crash at {start_sample/sr:.1f}s")
                    
                    # SKIP AHEAD 6 SECONDS so we don't extract the same crash twice
                    start_sample += int(6.0 * sr)
                else:
                    # Move forward slightly and check again
                    start_sample += int(0.5 * sr)
                        
        except Exception as e:
            print(f"Failed to process {wav_file}: {e}")
            
    print(f"Successfully generated {count} highly diverse crash samples.")

if __name__ == "__main__":
    download_audio()
    process_audio()
    print(f"Finished building dataset in {DATASET_DIR}")
    
    if os.path.exists(TEMP_YOUTUBE_DIR):
        shutil.rmtree(TEMP_YOUTUBE_DIR)

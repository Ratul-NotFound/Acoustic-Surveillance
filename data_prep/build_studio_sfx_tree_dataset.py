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
TEMP_SFX_DIR = "E:/software/acoustic-surveillance/data_prep/temp_tree_sfx"
ENV_DIR = "E:/software/acoustic-surveillance/data_prep/q1_dataset/00_forest_natural_environment_sound"
SR = 16000

print("Clearing old tree falling dataset...")
if os.path.exists(DATASET_DIR):
    shutil.rmtree(DATASET_DIR)
os.makedirs(DATASET_DIR, exist_ok=True)

if os.path.exists(TEMP_SFX_DIR):
    shutil.rmtree(TEMP_SFX_DIR)
os.makedirs(TEMP_SFX_DIR, exist_ok=True)

# 8 dedicated studio sound effect clips (100% clean sound effects)
SFX_URLS = [
    "https://www.youtube.com/watch?v=NpLE2-ZUzxc",
    "https://www.youtube.com/watch?v=QDGyPGLGQNw",
    "https://www.youtube.com/watch?v=hExOFTpTLLI",
    "https://www.youtube.com/watch?v=su2oT3s4fQ0",
    "https://www.youtube.com/watch?v=sLifNslAkWI",
    "https://www.youtube.com/watch?v=YeCqqDIZHS8",
    "https://www.youtube.com/watch?v=sUp9iGfNB1A",
    "https://www.youtube.com/watch?v=SnwuhzRDII8"
]

def load_random_env(duration=1.5):
    files = glob.glob(os.path.join(ENV_DIR, "*.wav"))
    if not files:
        return np.zeros(int(duration * SR))
    
    file = random.choice(files)
    y, _ = librosa.load(file, sr=SR, mono=True)
    
    length = int(duration * SR)
    if len(y) > length:
        start = random.randint(0, len(y) - length)
        y = y[start:start+length]
    else:
        y = np.pad(y, (0, length - len(y)))
    return y

def download_sfx():
    print("Downloading 8 dedicated studio sound effect clips...")
    for url in SFX_URLS:
        cmd = [
            "python", "-m", "yt_dlp",
            "--extract-audio",
            "--audio-format", "wav",
            "--ffmpeg-location", ffmpeg_dir,
            "--output", os.path.join(TEMP_SFX_DIR, "%(id)s.%(ext)s"),
            url
        ]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
        except Exception as e:
            print(f"Error downloading {url}: {e}")

def augment_and_save(segment, count):
    target_len = int(1.5 * SR)
    if len(segment) < target_len:
        segment = np.pad(segment, (0, target_len - len(segment)))
    else:
        segment = segment[:target_len]
        
    # Generate 4 augmented variations for each extracted chunk
    # 1. Clean segment + forest ambience
    env1 = load_random_env(1.5)
    mix1 = segment * 0.9 + env1 * random.uniform(0.1, 0.3)
    max1 = np.max(np.abs(mix1))
    if max1 > 0: mix1 = mix1 / max1 * 0.9
    sf.write(os.path.join(DATASET_DIR, f"sfx_tree_{count:04d}.wav"), mix1, SR)
    count += 1

    # 2. Pitch shift down (simulates massive heavy oak tree)
    shifted_down = librosa.effects.pitch_shift(segment, sr=SR, n_steps=random.uniform(-4, -1.5))
    env2 = load_random_env(1.5)
    mix2 = shifted_down * 0.9 + env2 * random.uniform(0.1, 0.3)
    max2 = np.max(np.abs(mix2))
    if max2 > 0: mix2 = mix2 / max2 * 0.9
    sf.write(os.path.join(DATASET_DIR, f"sfx_tree_{count:04d}.wav"), mix2, SR)
    count += 1

    # 3. Pitch shift up (simulates smaller pine/fir tree)
    shifted_up = librosa.effects.pitch_shift(segment, sr=SR, n_steps=random.uniform(1.5, 4))
    env3 = load_random_env(1.5)
    mix3 = shifted_up * 0.9 + env3 * random.uniform(0.1, 0.3)
    max3 = np.max(np.abs(mix3))
    if max3 > 0: mix3 = mix3 / max3 * 0.9
    sf.write(os.path.join(DATASET_DIR, f"sfx_tree_{count:04d}.wav"), mix3, SR)
    count += 1

    # 4. Slightly stretched / slowed down crash
    stretched = librosa.effects.time_stretch(segment, rate=random.uniform(0.8, 0.95))
    if len(stretched) < target_len:
        stretched = np.pad(stretched, (0, target_len - len(stretched)))
    else:
        stretched = stretched[:target_len]
    env4 = load_random_env(1.5)
    mix4 = stretched * 0.9 + env4 * random.uniform(0.1, 0.3)
    max4 = np.max(np.abs(mix4))
    if max4 > 0: mix4 = mix4 / max4 * 0.9
    sf.write(os.path.join(DATASET_DIR, f"sfx_tree_{count:04d}.wav"), mix4, SR)
    count += 1

    return count

def process_audio():
    print("Processing studio SFX clips into dataset samples...")
    wav_files = glob.glob(os.path.join(TEMP_SFX_DIR, "*.wav"))
    count = 0
    
    for wav_file in wav_files:
        print(f"Processing {os.path.basename(wav_file)}...")
        try:
            y, sr = librosa.load(wav_file, sr=SR, mono=True)
            chunk_samples = int(1.5 * SR)
            step = int(0.5 * SR)
            
            if len(y) <= chunk_samples:
                count = augment_and_save(y, count)
            else:
                for start_sample in range(0, len(y) - chunk_samples + 1, step):
                    segment = y[start_sample:start_sample + chunk_samples]
                    rms = librosa.feature.rms(y=segment)[0]
                    if np.max(rms) > 0.02: # capture cracking/crashing audio
                        count = augment_and_save(segment, count)
                        
        except Exception as e:
            print(f"Error processing {wav_file}: {e}")
            
    print(f"Total studio SFX dataset samples generated: {count}")

if __name__ == "__main__":
    download_sfx()
    process_audio()
    print(f"Finished building studio SFX dataset in {DATASET_DIR}")
    
    if os.path.exists(TEMP_SFX_DIR):
        shutil.rmtree(TEMP_SFX_DIR)

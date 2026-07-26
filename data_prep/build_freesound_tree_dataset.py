import os
import glob
import shutil
import urllib.request
import re
import random
import librosa
import soundfile as sf
import numpy as np

DATASET_DIR = "E:/software/acoustic-surveillance/data_prep/q1_dataset/tree_falling"
TEMP_FS_DIR = "E:/software/acoustic-surveillance/data_prep/temp_freesound_downloads"
ENV_DIR = "E:/software/acoustic-surveillance/data_prep/q1_dataset/00_forest_natural_environment_sound"
SR = 16000

print("Clearing old tree falling dataset...")
if os.path.exists(DATASET_DIR):
    shutil.rmtree(DATASET_DIR)
os.makedirs(DATASET_DIR, exist_ok=True)

if os.path.exists(TEMP_FS_DIR):
    shutil.rmtree(TEMP_FS_DIR)
os.makedirs(TEMP_FS_DIR, exist_ok=True)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
search_urls = [
    'https://freesound.org/search/?q=tree+falling',
    'https://freesound.org/search/?q=tree+felling',
    'https://freesound.org/search/?q=timber+crash',
    'https://freesound.org/search/?q=wood+crack+fall'
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

def collect_freesound_links():
    print("Collecting direct Freesound preview URLs...")
    links = []
    for url in search_urls:
        try:
            req = urllib.request.Request(url, headers=headers)
            html = urllib.request.urlopen(req).read().decode('utf-8')
            found = re.findall(r'https://cdn\.freesound\.org/previews/[^\"]+\.(?:mp3|ogg)', html)
            links.extend(found)
        except Exception as e:
            print(f"Error fetching search page {url}: {e}")
            
    links = list(set(links))
    print(f"Found {len(links)} unique Freesound audio links!")
    return links

def download_freesound_files(links):
    print("Downloading Freesound audio files...")
    downloaded_files = []
    for i, link in enumerate(links):
        ext = ".mp3" if link.endswith(".mp3") else ".ogg"
        out_path = os.path.join(TEMP_FS_DIR, f"fs_{i:03d}{ext}")
        try:
            req = urllib.request.Request(link, headers=headers)
            with urllib.request.urlopen(req) as resp, open(out_path, 'wb') as out_f:
                out_f.write(resp.read())
            downloaded_files.append(out_path)
        except Exception as e:
            pass
            
    print(f"Successfully downloaded {len(downloaded_files)} clean audio files from Freesound!")
    return downloaded_files

def process_and_build(downloaded_files):
    print("Processing Freesound field recordings into dataset samples...")
    count = 0
    chunk_samples = int(1.5 * SR)
    
    for audio_path in downloaded_files:
        try:
            y, sr = librosa.load(audio_path, sr=SR, mono=True)
            if len(y) < int(0.5 * SR):
                continue
                
            # If shorter than 1.5s, pad
            if len(y) <= chunk_samples:
                segments = [y]
            else:
                # Find RMS volume peaks (impacts)
                rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=512)[0]
                peak_indices = np.where(rms > np.percentile(rms, 70))[0] * 512
                
                filtered_peaks = []
                last_p = -3 * SR
                for p in peak_indices:
                    if p - last_p >= 3 * SR and p + chunk_samples <= len(y):
                        filtered_peaks.append(p)
                        last_p = p
                        
                segments = [y[p:p + chunk_samples] for p in filtered_peaks]
                if not segments:
                    segments = [y[:chunk_samples]]
                    
            for seg in segments:
                if len(seg) < chunk_samples:
                    seg = np.pad(seg, (0, chunk_samples - len(seg)))
                else:
                    seg = seg[:chunk_samples]
                    
                # Variation 1: Clean Freesound field recording + ambient forest
                env1 = load_random_env(1.5)
                mix1 = seg * 0.9 + env1 * random.uniform(0.05, 0.2)
                max1 = np.max(np.abs(mix1))
                if max1 > 0: mix1 = mix1 / max1 * 0.95
                sf.write(os.path.join(DATASET_DIR, f"freesound_tree_{count:04d}.wav"), mix1, SR)
                count += 1
                
                if count >= 200:
                    print(f"Successfully generated {count} pristine Freesound tree falling samples!")
                    return count
                    
                # Variation 2: Slightly pitch-shifted variation
                y_shift = librosa.effects.pitch_shift(seg, sr=SR, n_steps=random.uniform(-2, 2))
                env2 = load_random_env(1.5)
                mix2 = y_shift * 0.9 + env2 * random.uniform(0.05, 0.2)
                max2 = np.max(np.abs(mix2))
                if max2 > 0: mix2 = mix2 / max2 * 0.95
                sf.write(os.path.join(DATASET_DIR, f"freesound_tree_{count:04d}.wav"), mix2, SR)
                count += 1
                
                if count >= 200:
                    print(f"Successfully generated {count} pristine Freesound tree falling samples!")
                    return count

        except Exception as e:
            pass
            
    print(f"Total Freesound dataset samples created: {count}")
    return count

if __name__ == "__main__":
    links = collect_freesound_links()
    downloaded_files = download_freesound_files(links)
    total = process_and_build(downloaded_files)
    print(f"Finished building Freesound tree falling dataset ({total} samples) in {DATASET_DIR}")
    
    if os.path.exists(TEMP_FS_DIR):
        shutil.rmtree(TEMP_FS_DIR)

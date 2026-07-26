import os
import glob
import shutil
import subprocess
import librosa
import soundfile as sf
import numpy as np
import random
import scipy.signal as signal

ffmpeg_dir = r"C:\Users\mhrat\AppData\Local\ffmpegio\ffmpeg-downloader\ffmpeg\bin"
os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")

DATASET_DIR = "E:/software/acoustic-surveillance/data_prep/q1_dataset/tree_falling"
TEMP_REAL_DIR = "E:/software/acoustic-surveillance/data_prep/temp_real_tree_videos"
ENV_DIR = "E:/software/acoustic-surveillance/data_prep/q1_dataset/00_forest_natural_environment_sound"
SR = 16000

print("Clearing old dataset...")
if os.path.exists(DATASET_DIR):
    shutil.rmtree(DATASET_DIR)
os.makedirs(DATASET_DIR, exist_ok=True)

# 12 verified real-world tree felling video URLs
REAL_VIDEO_URLS = [
    "https://www.youtube.com/watch?v=i3b7WpFJGtg",
    "https://www.youtube.com/watch?v=pZU1UAeKAXM",
    "https://www.youtube.com/watch?v=pWqv1WHwo4M",
    "https://www.youtube.com/watch?v=6Ow45l7iQHY",
    "https://www.youtube.com/watch?v=HNn6Td1FOcU",
    "https://www.youtube.com/watch?v=Os2vrOT8F1Q",
    "https://www.youtube.com/watch?v=XxfHpSfIKRs",
    "https://www.youtube.com/watch?v=k3OcpBXyIk8",
    "https://www.youtube.com/watch?v=3mTd8ZTG_cc",
    "https://www.youtube.com/watch?v=3cbaDUCs414",
    "https://www.youtube.com/watch?v=kFHVnJjIysM",
    "https://www.youtube.com/watch?v=cm6W5OFBV84"
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

def download_videos():
    if not os.path.exists(TEMP_REAL_DIR):
        os.makedirs(TEMP_REAL_DIR, exist_ok=True)
    
    existing = glob.glob(os.path.join(TEMP_REAL_DIR, "*.wav"))
    if len(existing) >= 5:
        print(f"Using {len(existing)} previously downloaded real video files...")
        return

    print(f"Downloading {len(REAL_VIDEO_URLS)} distinct real-world tree felling videos...")
    for i, url in enumerate(REAL_VIDEO_URLS):
        cmd = [
            "python", "-m", "yt_dlp",
            "--extract-audio",
            "--audio-format", "wav",
            "--ffmpeg-location", ffmpeg_dir,
            "--output", os.path.join(TEMP_REAL_DIR, f"real_vid_{i:02d}.%(ext)s"),
            url
        ]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
            print(f"Downloaded real video {i+1}/{len(REAL_VIDEO_URLS)}")
        except Exception as e:
            print(f"Error downloading video {i+1}: {e}")

def apply_acoustic_variations(segment):
    target_len = int(1.5 * SR)
    if len(segment) < target_len:
        segment = np.pad(segment, (0, target_len - len(segment)))
    else:
        segment = segment[:target_len]

    # Variation 1: Clean real recording + subtle forest ambience
    env1 = load_random_env(1.5)
    mix1 = segment * 0.9 + env1 * random.uniform(0.05, 0.2)
    max1 = np.max(np.abs(mix1))
    if max1 > 0: mix1 = mix1 / max1 * 0.95

    # Variation 2: Distant recording (low-pass filter for air absorption)
    cutoff = random.uniform(2500, 4500)
    sos = signal.butter(4, cutoff, btype='lowpass', fs=SR, output='sos')
    distant = signal.sosfilt(sos, segment)
    env2 = load_random_env(1.5)
    mix2 = distant * 0.85 + env2 * random.uniform(0.1, 0.25)
    max2 = np.max(np.abs(mix2))
    if max2 > 0: mix2 = mix2 / max2 * 0.95

    return [mix1, mix2]

def extract_and_build():
    print("Extracting unique tree felling impacts across all downloaded videos...")
    wav_files = glob.glob(os.path.join(TEMP_REAL_DIR, "*.wav"))
    count = 0
    chunk_samples = int(1.5 * SR)
    
    for wav_file in wav_files:
        print(f"Processing real video source: {os.path.basename(wav_file)}...")
        try:
            y, sr = librosa.load(wav_file, sr=SR, mono=True)
            
            # Find transient peaks (crash/crack impacts)
            rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=512)[0]
            peak_indices = np.where(rms > np.percentile(rms, 85))[0] * 512
            
            # Filter peaks so we skip at least 6.0 seconds between extractions
            filtered_peaks = []
            last_p = -6 * SR
            for p in peak_indices:
                if p - last_p >= 6 * SR and p + chunk_samples <= len(y):
                    filtered_peaks.append(p)
                    last_p = p
                    
            for p in filtered_peaks:
                segment = y[p:p + chunk_samples]
                variations = apply_acoustic_variations(segment)
                for var in variations:
                    out_path = os.path.join(DATASET_DIR, f"real_tree_{count:04d}.wav")
                    sf.write(out_path, var, SR)
                    count += 1
                    
                    if count >= 200:
                        print(f"Successfully created {count} unique real-world samples!")
                        return count
                        
        except Exception as e:
            print(f"Error processing {wav_file}: {e}")
            
    print(f"Total unique real-world dataset samples created: {count}")
    return count

if __name__ == "__main__":
    download_videos()
    total_samples = extract_and_build()
    print(f"Finished building multi-source real-world dataset ({total_samples} samples) in {DATASET_DIR}")
    
    if os.path.exists(TEMP_REAL_DIR):
        shutil.rmtree(TEMP_REAL_DIR)

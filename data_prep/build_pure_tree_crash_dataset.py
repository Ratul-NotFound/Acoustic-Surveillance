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
CHAINSAW_DIR = "E:/software/acoustic-surveillance/data_prep/q1_dataset/chainsaw"
HANDSAW_DIR = "E:/software/acoustic-surveillance/data_prep/q1_dataset/handsaw"
TEMP_CRASH_DIR = "E:/software/acoustic-surveillance/data_prep/temp_tree_crash_videos"
ENV_DIR = "E:/software/acoustic-surveillance/data_prep/q1_dataset/00_forest_natural_environment_sound"
SR = 16000

print("Clearing old tree falling dataset...")
if os.path.exists(DATASET_DIR):
    shutil.rmtree(DATASET_DIR)
os.makedirs(DATASET_DIR, exist_ok=True)

# 10 dedicated pure tree crash SFX videos
PURE_CRASH_URLS = [
    "https://www.youtube.com/watch?v=WDTWu7FYqOo",
    "https://www.youtube.com/watch?v=NpLE2-ZUzxc",
    "https://www.youtube.com/watch?v=QDGyPGLGQNw",
    "https://www.youtube.com/watch?v=hExOFTpTLLI",
    "https://www.youtube.com/watch?v=su2oT3s4fQ0",
    "https://www.youtube.com/watch?v=YeCqqDIZHS8",
    "https://www.youtube.com/watch?v=pib4ID4p-i0",
    "https://www.youtube.com/watch?v=5_DuqVpAOJM",
    "https://www.youtube.com/watch?v=mLdc7kKid6I",
    "https://www.youtube.com/watch?v=v0eC5GI33AM"
]

# Load chainsaw reference profile for motor noise rejection
print("Loading chainsaw reference profile for motor rejection filter...")
saw_files = glob.glob(os.path.join(CHAINSAW_DIR, "*.wav"))[:20] + glob.glob(os.path.join(HANDSAW_DIR, "*.wav"))[:10]
saw_mfccs = []
for sf_file in saw_files:
    try:
        y_saw, _ = librosa.load(sf_file, sr=SR, mono=True)
        mfcc_saw = librosa.feature.mfcc(y=y_saw, sr=SR, n_mfcc=13)
        saw_mfccs.append(np.mean(mfcc_saw, axis=1))
    except:
        pass

REF_SAW_MFCC = np.mean(saw_mfccs, axis=0) if saw_mfccs else None

def is_cutting_noise(segment):
    """Detect if segment contains chainsaw motor revs or saw cutting noise."""
    if REF_SAW_MFCC is None:
        return False
        
    try:
        # Check MFCC cosine similarity to chainsaw reference
        mfcc_seg = np.mean(librosa.feature.mfcc(y=segment, sr=SR, n_mfcc=13), axis=1)
        sim = np.dot(mfcc_seg, REF_SAW_MFCC) / (np.linalg.norm(mfcc_seg) * np.linalg.norm(REF_SAW_MFCC) + 1e-8)
        
        # Chainsaw motors have high harmonic energy and continuous pitch in 100-600Hz
        y_harm, y_perc = librosa.effects.hpss(segment)
        harm_ratio = np.sum(y_harm**2) / (np.sum(segment**2) + 1e-8)
        
        # If high similarity to chainsaw AND high harmonic motor ratio, reject!
        if sim > 0.88 and harm_ratio > 0.50:
            return True
            
    except Exception:
        pass
        
    return False

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
    if not os.path.exists(TEMP_CRASH_DIR):
        os.makedirs(TEMP_CRASH_DIR, exist_ok=True)
    
    existing = glob.glob(os.path.join(TEMP_CRASH_DIR, "*.wav"))
    if len(existing) >= 5:
        print(f"Using {len(existing)} previously downloaded crash SFX files...")
        return

    print(f"Downloading {len(PURE_CRASH_URLS)} pure tree crash SFX videos...")
    for i, url in enumerate(PURE_CRASH_URLS):
        cmd = [
            "python", "-m", "yt_dlp",
            "--extract-audio",
            "--audio-format", "wav",
            "--ffmpeg-location", ffmpeg_dir,
            "--output", os.path.join(TEMP_CRASH_DIR, f"crash_vid_{i:02d}.%(ext)s"),
            url
        ]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
            print(f"Downloaded crash video {i+1}/{len(PURE_CRASH_URLS)}")
        except Exception as e:
            print(f"Error downloading video {i+1}: {e}")

def apply_acoustic_variations(segment):
    target_len = int(1.5 * SR)
    if len(segment) < target_len:
        segment = np.pad(segment, (0, target_len - len(segment)))
    else:
        segment = segment[:target_len]

    # Variation 1: Clean tree crash + subtle forest ambience
    env1 = load_random_env(1.5)
    mix1 = segment * 0.9 + env1 * random.uniform(0.05, 0.2)
    max1 = np.max(np.abs(mix1))
    if max1 > 0: mix1 = mix1 / max1 * 0.95

    # Variation 2: Heavy oak crash (pitch-shifted slightly down)
    shifted_down = librosa.effects.pitch_shift(segment, sr=SR, n_steps=random.uniform(-3, -1))
    env2 = load_random_env(1.5)
    mix2 = shifted_down * 0.9 + env2 * random.uniform(0.05, 0.2)
    max2 = np.max(np.abs(mix2))
    if max2 > 0: mix2 = mix2 / max2 * 0.95

    # Variation 3: Distant crash (low-pass filter for air absorption)
    cutoff = random.uniform(2500, 4500)
    sos = signal.butter(4, cutoff, btype='lowpass', fs=SR, output='sos')
    distant = signal.sosfilt(sos, segment)
    env3 = load_random_env(1.5)
    mix3 = distant * 0.85 + env3 * random.uniform(0.1, 0.25)
    max3 = np.max(np.abs(mix3))
    if max3 > 0: mix3 = mix3 / max3 * 0.95

    return [mix1, mix2, mix3]

def extract_pure_crash_dataset():
    print("Extracting PURE tree crash impacts (filtering out chainsaw & saw cutting noise)...")
    wav_files = glob.glob(os.path.join(TEMP_CRASH_DIR, "*.wav"))
    count = 0
    chunk_samples = int(1.5 * SR)
    rejected_count = 0
    
    for wav_file in wav_files:
        print(f"Processing crash source: {os.path.basename(wav_file)}...")
        try:
            y, sr = librosa.load(wav_file, sr=SR, mono=True)
            if len(y) <= chunk_samples:
                segments = [y]
            else:
                rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=512)[0]
                peak_indices = np.where(rms > np.percentile(rms, 65))[0] * 512
                
                filtered_peaks = []
                last_p = -2 * SR
                for p in peak_indices:
                    if p - last_p >= 2 * SR and p + chunk_samples <= len(y):
                        filtered_peaks.append(p)
                        last_p = p
                        
                segments = [y[p:p + chunk_samples] for p in filtered_peaks]
                if not segments:
                    segments = [y[:chunk_samples]]
                    
            for seg in segments:
                # RUN CHAINSAW / CUTTING NOISE REJECTION FILTER
                if is_cutting_noise(seg):
                    rejected_count += 1
                    continue # REJECT CHAINSAW NOISE!
                    
                variations = apply_acoustic_variations(seg)
                for var in variations:
                    out_path = os.path.join(DATASET_DIR, f"pure_tree_crash_{count:04d}.wav")
                    sf.write(out_path, var, SR)
                    count += 1
                    
                    if count >= 200:
                        print(f"Successfully generated {count} PURE tree crash samples! (Rejected {rejected_count} cutting noise segments)")
                        return count
                        
        except Exception as e:
            print(f"Error processing {wav_file}: {e}")
            
    print(f"Total pure tree crash dataset samples created: {count} (Rejected {rejected_count} cutting noise segments)")
    return count

if __name__ == "__main__":
    download_videos()
    total_samples = extract_pure_crash_dataset()
    print(f"Finished building pure tree crash dataset ({total_samples} samples) in {DATASET_DIR}")
    
    if os.path.exists(TEMP_CRASH_DIR):
        shutil.rmtree(TEMP_CRASH_DIR)

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
SPEECH_DIR = "E:/software/acoustic-surveillance/data_prep/q1_dataset/human_speech"
TEMP_REAL_DIR = "E:/software/acoustic-surveillance/data_prep/temp_real_tree_videos"
ENV_DIR = "E:/software/acoustic-surveillance/data_prep/q1_dataset/00_forest_natural_environment_sound"
SR = 16000

print("Clearing old tree falling dataset...")
if os.path.exists(DATASET_DIR):
    shutil.rmtree(DATASET_DIR)
os.makedirs(DATASET_DIR, exist_ok=True)

# 12 real-world field videos
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

# Load human speech reference profile for voice rejection
print("Loading human speech reference profile for speech rejection filter...")
speech_files = glob.glob(os.path.join(SPEECH_DIR, "*.wav"))[:20]
speech_mfccs = []
for sf_file in speech_files:
    try:
        y_sp, _ = librosa.load(sf_file, sr=SR, mono=True)
        mfcc_sp = librosa.feature.mfcc(y=y_sp, sr=SR, n_mfcc=13)
        speech_mfccs.append(np.mean(mfcc_sp, axis=1))
    except:
        pass

REF_SPEECH_MFCC = np.mean(speech_mfccs, axis=0) if speech_mfccs else None

def is_human_speech(segment):
    """Detect if segment contains human speech based on MFCC similarity & vocal pitch activity."""
    if REF_SPEECH_MFCC is None:
        return False
        
    try:
        # Check MFCC cosine similarity to human speech reference
        mfcc_seg = np.mean(librosa.feature.mfcc(y=segment, sr=SR, n_mfcc=13), axis=1)
        sim = np.dot(mfcc_seg, REF_SPEECH_MFCC) / (np.linalg.norm(mfcc_seg) * np.linalg.norm(REF_SPEECH_MFCC) + 1e-8)
        
        # Check harmonic ratio (speech has high harmonic energy in 100Hz-3000Hz)
        y_harm, y_perc = librosa.effects.hpss(segment)
        harm_ratio = np.sum(y_harm**2) / (np.sum(segment**2) + 1e-8)
        
        # If high similarity to speech AND high harmonic ratio, it's human voice!
        if sim > 0.85 and harm_ratio > 0.45:
            return True
            
        # Check vocal pitch presence using pyin
        f0, voiced_flag, _ = librosa.pyin(segment, fmin=80, fmax=400, sr=SR)
        voiced_ratio = np.nanmean(voiced_flag) if voiced_flag is not None else 0
        if voiced_ratio > 0.4:
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
    if not os.path.exists(TEMP_REAL_DIR):
        os.makedirs(TEMP_REAL_DIR, exist_ok=True)
    
    existing = glob.glob(os.path.join(TEMP_REAL_DIR, "*.wav"))
    if len(existing) >= 5:
        print(f"Using {len(existing)} previously downloaded field videos...")
        return

    print(f"Downloading {len(REAL_VIDEO_URLS)} real-world tree felling field videos...")
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
            print(f"Downloaded field video {i+1}/{len(REAL_VIDEO_URLS)}")
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

def extract_speech_free_dataset():
    print("Extracting SPEECH-FREE tree felling impacts...")
    wav_files = glob.glob(os.path.join(TEMP_REAL_DIR, "*.wav"))
    count = 0
    chunk_samples = int(1.5 * SR)
    rejected_count = 0
    
    for wav_file in wav_files:
        print(f"Scanning field video: {os.path.basename(wav_file)}...")
        try:
            y, sr = librosa.load(wav_file, sr=SR, mono=True)
            
            # Find transient peaks (crash/crack impacts)
            rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=512)[0]
            peak_indices = np.where(rms > np.percentile(rms, 80))[0] * 512
            
            # Filter peaks with 4.0s minimum spacing
            filtered_peaks = []
            last_p = -4 * SR
            for p in peak_indices:
                if p - last_p >= 4 * SR and p + chunk_samples <= len(y):
                    filtered_peaks.append(p)
                    last_p = p
                    
            for p in filtered_peaks:
                segment = y[p:p + chunk_samples]
                
                # RUN SPEECH REJECTION FILTER
                if is_human_speech(segment):
                    rejected_count += 1
                    continue # REJECT SPEECH!
                    
                variations = apply_acoustic_variations(segment)
                for var in variations:
                    out_path = os.path.join(DATASET_DIR, f"speech_free_tree_{count:04d}.wav")
                    sf.write(out_path, var, SR)
                    count += 1
                    
                    if count >= 200:
                        print(f"Successfully generated {count} SPEECH-FREE tree falling samples! (Rejected {rejected_count} speech segments)")
                        return count
                        
        except Exception as e:
            print(f"Error processing {wav_file}: {e}")
            
    print(f"Total speech-free dataset samples created: {count} (Rejected {rejected_count} speech segments)")
    return count

if __name__ == "__main__":
    download_videos()
    total_samples = extract_speech_free_dataset()
    print(f"Finished building speech-free dataset ({total_samples} samples) in {DATASET_DIR}")
    
    if os.path.exists(TEMP_REAL_DIR):
        shutil.rmtree(TEMP_REAL_DIR)

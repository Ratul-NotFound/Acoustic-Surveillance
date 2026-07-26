import os
import glob
import shutil
import random
import librosa
import soundfile as sf
import numpy as np
import scipy.signal as signal

DATASET_DIR = "E:/software/acoustic-surveillance/data_prep/q1_dataset/tree_falling"
AXE_DIR = "E:/software/acoustic-surveillance/data_prep/q1_dataset/axe_machete_chopping"
ENV_DIR = "E:/software/acoustic-surveillance/data_prep/q1_dataset/00_forest_natural_environment_sound"
SR = 16000
DURATION = 3.0
TOTAL_SAMPLES = int(SR * DURATION)

print("Clearing old tree falling dataset...")
if os.path.exists(DATASET_DIR):
    shutil.rmtree(DATASET_DIR)
os.makedirs(DATASET_DIR, exist_ok=True)

def load_random_snippet(directory, duration=1.0):
    files = glob.glob(os.path.join(directory, "*.wav"))
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

def generate_timber_creak(dur=0.8):
    # Wood groan/creak under intense bending tension
    length = int(dur * SR)
    t = np.linspace(0, dur, length, endpoint=False)
    
    # Low frequency wood groan
    freq = random.uniform(150, 350)
    groan = np.sin(2 * np.pi * freq * t + 0.5 * np.sin(2 * np.pi * 15 * t))
    
    # Splinter snaps
    num_snaps = random.randint(4, 10)
    snaps = np.zeros(length)
    for _ in range(num_snaps):
        idx = random.randint(0, length - 500)
        snap_noise = np.random.normal(0, 1, 500)
        snap_env = np.exp(-np.linspace(0, 10, 500))
        snaps[idx:idx+500] += snap_noise * snap_env
        
    sos = signal.butter(4, [300, 3000], btype='bandpass', fs=SR, output='sos')
    snaps = signal.sosfilt(sos, snaps)
    
    env = np.exp(-t * 2.5) * (t / dur)
    return (groan * 0.4 + snaps * 0.8) * env

def generate_canopy_rush(dur=1.2):
    # Branches/leaves rushing through the air during fall
    length = int(dur * SR)
    white = np.random.normal(0, 1, length)
    
    sos = signal.butter(4, [1500, 6500], btype='bandpass', fs=SR, output='sos')
    rush = signal.sosfilt(sos, white)
    
    t = np.linspace(0, 1, length)
    envelope = np.sin(t * np.pi) ** 2
    return rush * envelope * random.uniform(0.3, 0.6)

def generate_ground_crash(dur=1.0):
    # Heavy trunk impact + branch snapping
    length = int(dur * SR)
    t = np.linspace(0, dur, length, endpoint=False)
    
    # Deep bass earth thud (80Hz -> 25Hz)
    boom_freqs = np.linspace(80, 25, length)
    phase = 2 * np.pi * np.cumsum(boom_freqs) / SR
    boom = np.sin(phase)
    
    # Low-passed impact noise
    impact_noise = np.random.normal(0, 1, length)
    sos_low = signal.butter(4, 250, btype='lowpass', fs=SR, output='sos')
    thud = signal.sosfilt(sos_low, impact_noise)
    
    # Branch breaking crunch (bandpassed high noise spikes)
    crunch_noise = np.random.normal(0, 1, length)
    sos_high = signal.butter(4, [800, 4500], btype='bandpass', fs=SR, output='sos')
    crunch = signal.sosfilt(sos_high, crunch_noise)
    
    decay = np.exp(-t * random.uniform(5, 8))
    impact = (boom * 0.6 + thud * 1.2 + crunch * 0.8) * decay
    return impact

def build_single_felling_sample():
    audio = np.zeros(TOTAL_SAMPLES)
    
    # 1. Final Chop / Cut (0.0s - 0.4s)
    chop = load_random_snippet(AXE_DIR, duration=0.4)
    audio[:len(chop)] += chop * random.uniform(0.7, 1.1)
    
    # 2. Wood Creak / Tension Splintering (0.3s - 1.1s)
    creak = generate_timber_creak(dur=0.8)
    start_c = int(0.3 * SR)
    audio[start_c:start_c+len(creak)] += creak * random.uniform(0.7, 1.2)
    
    # 3. Canopy Rush / Leaves Swishing (0.9s - 2.1s)
    rush = generate_canopy_rush(dur=1.2)
    start_r = int(0.9 * SR)
    audio[start_r:start_r+len(rush)] += rush * random.uniform(0.6, 1.0)
    
    # 4. Ground Crash & Branch Breaking (1.8s - 2.8s)
    crash = generate_ground_crash(dur=1.0)
    start_cr = int(1.8 * SR)
    audio[start_cr:start_cr+len(crash)] += crash * random.uniform(0.8, 1.3)
    
    # 5. Forest Ambient Layering
    env = load_random_snippet(ENV_DIR, duration=DURATION)
    audio = audio + env * random.uniform(0.1, 0.3)
    
    # Normalize
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val * 0.95
        
    return audio

def build_dataset():
    num_samples = 200
    print(f"Generating {num_samples} full-sequence 'Tree Falling After Cut' audio samples...")
    
    for i in range(num_samples):
        sample = build_single_felling_sample()
        out_path = os.path.join(DATASET_DIR, f"tree_felling_after_cut_{i:04d}.wav")
        sf.write(out_path, sample, SR)
        if i % 25 == 0:
            print(f"Generated {i}/{num_samples} samples...")
            
    print(f"Finished building dataset in {DATASET_DIR}")

if __name__ == "__main__":
    build_dataset()

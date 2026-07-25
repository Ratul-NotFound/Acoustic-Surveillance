import os
import glob
import shutil
import random
import librosa
import soundfile as sf
import numpy as np
import scipy.signal as signal

DATASET_DIR = "E:/software/acoustic-surveillance/data_prep/q1_dataset/tree_falling"
ENV_DIR = "E:/software/acoustic-surveillance/data_prep/q1_dataset/00_forest_natural_environment_sound"
SR = 16000

print("Clearing old noisy tree falling dataset...")
if os.path.exists(DATASET_DIR):
    shutil.rmtree(DATASET_DIR)
os.makedirs(DATASET_DIR, exist_ok=True)

def load_random_env(duration=3.0):
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

def generate_crack():
    # Simulate a single sharp crack/splinter of wood
    length = int(0.15 * SR)
    noise = np.random.normal(0, 1, length)
    
    # Sharp attack, fast exponential decay
    t = np.linspace(0, 1, length)
    envelope = np.exp(-t * 20)
    crack = noise * envelope
    
    # Bandpass to focus on the woody midrange (500Hz - 4kHz)
    sos = signal.butter(4, [500, 4000], btype='bandpass', fs=SR, output='sos')
    crack = signal.sosfilt(sos, crack)
    return crack

def synthesize_tree_fall(duration=3.0):
    total_samples = int(duration * SR)
    audio = np.zeros(total_samples)
    
    # Phase 1: Splintering & Cracking (0.0s to 1.5s)
    # Generate 5-15 random cracks, increasing in density and volume
    num_cracks = random.randint(5, 15)
    crack_times = np.linspace(0.2, 1.4, num_cracks)
    crack_times += np.random.normal(0, 0.1, num_cracks) # jitter
    
    for i, ct in enumerate(crack_times):
        if ct > 1.5 or ct < 0: continue
        crack = generate_crack()
        vol = (i / num_cracks) * random.uniform(0.5, 1.0) # crescendo
        start_idx = int(ct * SR)
        end_idx = start_idx + len(crack)
        if end_idx <= total_samples:
            audio[start_idx:end_idx] += crack * vol
            
    # Phase 2: The Whoosh / Leaves Swishing (1.0s to 2.0s)
    whoosh_dur = 1.0
    whoosh_samples = int(whoosh_dur * SR)
    white_noise = np.random.normal(0, 1, whoosh_samples)
    # Bandpass filter for leaves (2000Hz - 8000Hz)
    sos_whoosh = signal.butter(4, [2000, 7000], btype='bandpass', fs=SR, output='sos')
    whoosh = signal.sosfilt(sos_whoosh, white_noise)
    
    # Envelope for whoosh (fade in, hold, fade out)
    w_t = np.linspace(0, 1, whoosh_samples)
    w_env = np.sin(w_t * np.pi) ** 2
    whoosh = whoosh * w_env * random.uniform(0.2, 0.4)
    
    w_start = int(1.0 * SR)
    audio[w_start:w_start+whoosh_samples] += whoosh
    
    # Phase 3: The Massive Impact (1.8s)
    impact_start = int(1.8 * SR)
    impact_dur = 1.0
    impact_samples = int(impact_dur * SR)
    
    # Low frequency boom (sweep from 100Hz down to 20Hz)
    t_boom = np.linspace(0, impact_dur, impact_samples, endpoint=False)
    boom_freqs = np.linspace(100, 20, impact_samples)
    phase = 2 * np.pi * np.cumsum(boom_freqs) / SR
    boom = np.sin(phase)
    
    # Impact noise (low passed)
    impact_noise = np.random.normal(0, 1, impact_samples)
    sos_impact = signal.butter(4, 300, btype='lowpass', fs=SR, output='sos')
    thud_noise = signal.sosfilt(sos_impact, impact_noise)
    
    # Mix boom and thud
    impact = (boom * 0.5 + thud_noise * 1.5)
    
    # Impact Envelope (sharp attack, slow decay)
    imp_env = np.exp(-t_boom * random.uniform(4, 7))
    impact = impact * imp_env
    
    audio[impact_start:impact_start+impact_samples] += impact * random.uniform(0.8, 1.2)
    
    # Normalize the entire synthesized sound
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val * 0.95
        
    return audio

def build_dataset():
    num_samples = 200
    print(f"Synthesizing {num_samples} pristine tree falling DSP samples...")
    for i in range(num_samples):
        # 1. Synthesize the clean tree fall
        tree_audio = synthesize_tree_fall(duration=3.0)
        
        # 2. Add realistic forest background noise
        env_audio = load_random_env(duration=3.0)
        
        # 3. Mix
        mixed = tree_audio + env_audio * random.uniform(0.1, 0.4)
        
        # 4. Normalize
        max_val = np.max(np.abs(mixed))
        if max_val > 0:
            mixed = mixed / max_val * 0.95
            
        out_path = os.path.join(DATASET_DIR, f"dsp_tree_{i:04d}.wav")
        sf.write(out_path, mixed, SR)
        
        if i % 25 == 0:
            print(f"Generated {i}/{num_samples} samples...")
            
    print(f"Finished building flawless DSP dataset in {DATASET_DIR}")

if __name__ == "__main__":
    build_dataset()

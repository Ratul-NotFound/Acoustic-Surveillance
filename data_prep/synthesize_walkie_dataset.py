import os
import shutil
import numpy as np
import scipy.signal as signal
import soundfile as sf
import random

DATASET_DIR = "E:/software/acoustic-surveillance/data_prep/q1_dataset/walkie_talkie"
SR = 16000

# Ensure clean slate
print("Clearing old walkie talkie dataset...")
if os.path.exists(DATASET_DIR):
    shutil.rmtree(DATASET_DIR)
os.makedirs(DATASET_DIR, exist_ok=True)

def generate_squelch_beep(duration=1.0, sr=16000):
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    audio = np.zeros_like(t)
    
    # Randomize parameters for variety
    beep_freq = random.uniform(1200, 2500)
    beep_duration = random.uniform(0.05, 0.15)
    static_duration = random.uniform(0.3, 0.7)
    
    # 1. Start Beep (Sine Wave)
    beep_samples = int(beep_duration * sr)
    audio[:beep_samples] = 0.5 * np.sin(2 * np.pi * beep_freq * t[:beep_samples])
    
    # 2. Static / Squelch (Bandpass filtered white noise)
    static_start = beep_samples
    static_end = static_start + int(static_duration * sr)
    if static_end > len(audio):
        static_end = len(audio)
        
    noise = np.random.normal(0, 0.3, static_end - static_start)
    # Bandpass filter the noise to simulate radio bandwidth (300Hz - 3400Hz)
    sos = signal.butter(4, [300, 3400], btype='bandpass', fs=sr, output='sos')
    filtered_noise = signal.sosfilt(sos, noise)
    
    audio[static_start:static_end] = filtered_noise
    
    # 3. End Beep (optional, sometimes they have double beeps)
    if random.random() > 0.5:
        end_beep_start = static_end
        end_beep_end = end_beep_start + int(0.05 * sr)
        if end_beep_end < len(audio):
            audio[end_beep_start:end_beep_end] = 0.5 * np.sin(2 * np.pi * beep_freq * t[end_beep_start:end_beep_end])
            
    # Normalize
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val * 0.8
        
    return audio

def build_synthetic_dataset():
    num_samples = 300
    print(f"Synthesizing {num_samples} pure walkie-talkie squelches...")
    
    for i in range(num_samples):
        audio = generate_squelch_beep(duration=1.0, sr=SR)
        out_path = os.path.join(DATASET_DIR, f"synth_walkie_{i:04d}.wav")
        sf.write(out_path, audio, SR)
        
        if i % 50 == 0:
            print(f"Generated {i}/{num_samples} samples...")
            
    print(f"Finished building perfect synthetic dataset in {DATASET_DIR}")

if __name__ == "__main__":
    build_synthetic_dataset()

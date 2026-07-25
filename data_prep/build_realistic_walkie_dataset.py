import os
import glob
import shutil
import random
import librosa
import soundfile as sf
import numpy as np
import scipy.signal as signal

DATASET_DIR = "E:/software/acoustic-surveillance/data_prep/q1_dataset/walkie_talkie"
SPEECH_DIR = "E:/software/acoustic-surveillance/data_prep/q1_dataset/human_speech"
ENV_DIR = "E:/software/acoustic-surveillance/data_prep/q1_dataset/00_forest_natural_environment_sound"
SR = 16000

# Ensure clean slate
print("Clearing old dataset...")
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

def radio_dsp_effect(audio):
    # 1. Bandpass filter to simulate cheap radio speaker (300Hz - 3400Hz)
    sos = signal.butter(4, [300, 3400], btype='bandpass', fs=SR, output='sos')
    filtered = signal.sosfilt(sos, audio)
    
    # 2. Overdrive / Clipping distortion (walkie talkies are often loud and distorted)
    gain = random.uniform(2.0, 5.0)
    clipped = np.clip(filtered * gain, -0.8, 0.8)
    
    # 3. Downsample and upsample to simulate low bitrate digital radios (optional, randomly apply)
    if random.random() > 0.5:
        low_sr = 8000
        downsampled = librosa.resample(clipped, orig_sr=SR, target_sr=low_sr)
        clipped = librosa.resample(downsampled, orig_sr=low_sr, target_sr=SR)
        clipped = clipped[:len(audio)] # fix length differences
        
    return clipped

def generate_roger_beep():
    # Generate a very short burst of a sine wave (roger beep)
    beep_freq = random.uniform(1000, 2500)
    beep_duration = random.uniform(0.05, 0.15)
    t = np.linspace(0, beep_duration, int(SR * beep_duration), endpoint=False)
    beep = 0.5 * np.sin(2 * np.pi * beep_freq * t)
    return beep

def build_realistic_dataset():
    num_samples = 200
    print(f"Synthesizing {num_samples} highly realistic radio transmissions...")
    
    for i in range(num_samples):
        # 1. Grab random human speech
        speech = load_random_snippet(SPEECH_DIR, duration=1.0)
        
        # 2. Grab random background environment
        env = load_random_snippet(ENV_DIR, duration=1.0)
        
        # 3. Mix speech + background (before the mic)
        mixed = speech * random.uniform(0.6, 1.2) + env * random.uniform(0.1, 0.4)
        
        # 4. Apply Radio DSP (through the transmission)
        radio_transmission = radio_dsp_effect(mixed)
        
        # 5. Add static/squelch
        noise = np.random.normal(0, random.uniform(0.05, 0.2), len(radio_transmission))
        sos_noise = signal.butter(4, [300, 3400], btype='bandpass', fs=SR, output='sos')
        static = signal.sosfilt(sos_noise, noise)
        
        final_audio = radio_transmission + static
        
        # 6. Add Roger Beeps randomly at start or end
        if random.random() > 0.3:
            beep = generate_roger_beep()
            # replace start with beep
            final_audio[:len(beep)] = beep
        if random.random() > 0.5:
            beep = generate_roger_beep()
            # replace end with beep
            final_audio[-len(beep):] = beep
            
        # Normalize
        max_val = np.max(np.abs(final_audio))
        if max_val > 0:
            final_audio = final_audio / max_val * 0.9
            
        out_path = os.path.join(DATASET_DIR, f"real_walkie_dsp_{i:04d}.wav")
        sf.write(out_path, final_audio, SR)
        
        if i % 25 == 0:
            print(f"Generated {i}/{num_samples} samples...")
            
    print(f"Finished building perfect synthetic dataset in {DATASET_DIR}")

if __name__ == "__main__":
    build_realistic_dataset()

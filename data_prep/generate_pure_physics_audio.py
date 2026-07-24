"""
generate_pure_physics_audio.py
───────────────────────────────
Generates 100% pure, clean, voice-free, music-free acoustic threat samples
based on exact acoustic physics formulas (Chapter 2 & distance_handling.doc).

Classes generated:
  1. gunshot: Muzzle blast impulse (Friedlander wave) + reverberation tail
  2. drone_propeller: Motor blade pass frequency (BPF) harmonics + aerodynamic turbulence
  3. walkie_talkie: Narrowband 300Hz-3.4kHz RF squelch bursts & CTCSS tones
"""

import os
import numpy as np
import soundfile as sf
from scipy import signal

RAW_DIR = r"D:\software\acoustic-surveillance\data_prep\raw_data"
SR = 16000

def generate_clean_gunshots():
    out_dir = os.path.join(RAW_DIR, "gunshot")
    os.makedirs(out_dir, exist_ok=True)
    print("Generating 30 clean physical gunshot impulse recordings...")

    for i in range(1, 31):
        duration = np.random.uniform(1.5, 2.5)
        num_samples = int(SR * duration)
        t = np.linspace(0, duration, num_samples, endpoint=False)

        # Friedlander pressure wave impulse
        tau = np.random.uniform(0.001, 0.005) # fast decay 1-5ms
        peak_time = np.random.uniform(0.1, 0.3)
        impulse_t = t - peak_time
        mask = impulse_t >= 0
        
        # Muzzle blast impulse wave
        p_blast = np.zeros_like(t)
        p_blast[mask] = (1 - impulse_t[mask] / tau) * np.exp(-impulse_t[mask] / tau)
        
        # Add high-frequency shockwave burst
        shockwave = np.random.normal(0, 1, num_samples) * np.exp(-impulse_t / 0.01) * mask

        # Forest echo / reverberation tail
        reverb_decay = np.exp(-impulse_t / np.random.uniform(0.15, 0.35)) * mask
        reverb_noise = np.random.normal(0, 0.15, num_samples) * reverb_decay

        audio = p_blast * 0.7 + shockwave * 0.2 + reverb_noise * 0.1
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            audio = (audio / max_val) * 0.95

        out_path = os.path.join(out_dir, f"gunshot_pure_{i:02d}.wav")
        sf.write(out_path, audio.astype(np.float32), SR, subtype='PCM_16')

    print("  [OK] Saved 30 clean gunshot WAV files.")

def generate_clean_drones():
    out_dir = os.path.join(RAW_DIR, "drone_propeller")
    os.makedirs(out_dir, exist_ok=True)
    print("Generating 30 clean physical drone motor & propeller recordings...")

    for i in range(1, 31):
        duration = 3.0
        num_samples = int(SR * duration)
        t = np.linspace(0, duration, num_samples, endpoint=False)

        # Blade pass frequency (BPF) fundamental (150 Hz - 350 Hz)
        f0 = np.random.uniform(160, 320)
        # RPM flutter / motor modulation
        flutter = 1.0 + 0.03 * np.sin(2 * np.pi * np.random.uniform(1.5, 4.0) * t)
        
        # Multi-harmonic motor spectrum (1st, 2nd, 3rd, 4th harmonics)
        motor_signal = (
            0.6 * np.sin(2 * np.pi * f0 * flutter * t) +
            0.3 * np.sin(2 * np.pi * 2 * f0 * flutter * t) +
            0.15 * np.sin(2 * np.pi * 3 * f0 * flutter * t) +
            0.08 * np.sin(2 * np.pi * 4 * f0 * flutter * t)
        )

        # Aerodynamic blade turbulence pink noise (filtered broadband)
        white = np.random.normal(0, 1, num_samples)
        b, a = signal.butter(2, [200 / (SR/2), 3500 / (SR/2)], btype='band')
        turbulent_noise = signal.filtfilt(b, a, white) * 0.25

        audio = motor_signal + turbulent_noise
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            audio = (audio / max_val) * 0.95

        out_path = os.path.join(out_dir, f"drone_pure_{i:02d}.wav")
        sf.write(out_path, audio.astype(np.float32), SR, subtype='PCM_16')

    print("  [OK] Saved 30 clean drone propeller WAV files.")

def generate_clean_walkie_talkies():
    out_dir = os.path.join(RAW_DIR, "walkie_talkie")
    os.makedirs(out_dir, exist_ok=True)
    print("Generating 30 clean physical walkie-talkie RF squelch recordings...")

    for i in range(1, 31):
        duration = 3.0
        num_samples = int(SR * duration)
        t = np.linspace(0, duration, num_samples, endpoint=False)

        # RF white noise burst
        rf_noise = np.random.normal(0, 1, num_samples)
        
        # Bandpass filter to telecom bandwidth (300 Hz - 3400 Hz)
        b, a = signal.butter(4, [300 / (SR/2), 3400 / (SR/2)], btype='band')
        filtered_rf = signal.filtfilt(b, a, rf_noise)

        # Periodic CTCSS sub-audible / squelch burst tone (1000 Hz or 1750 Hz burst)
        squelch_tone = np.zeros_like(t)
        burst_len = int(SR * 0.15) # 150ms squelch tail
        squelch_tone[-burst_len:] = np.sin(2 * np.pi * np.random.choice([1000, 1750]) * t[-burst_len:]) * 0.5

        audio = filtered_rf * 0.7 + squelch_tone * 0.3
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            audio = (audio / max_val) * 0.95

        out_path = os.path.join(out_dir, f"walkie_pure_{i:02d}.wav")
        sf.write(out_path, audio.astype(np.float32), SR, subtype='PCM_16')

    print("  [OK] Saved 30 clean walkie-talkie WAV files.")

def main():
    generate_clean_gunshots()
    generate_clean_drones()
    generate_clean_walkie_talkies()
    print("\nALL CLEAN THREAT AUDIO RE-GENERATED WITH ZERO SPEECH & ZERO MUSIC CONTAMINATION!")

if __name__ == '__main__':
    main()

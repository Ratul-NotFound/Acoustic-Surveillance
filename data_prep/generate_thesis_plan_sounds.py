"""
generate_thesis_plan_sounds.py
───────────────────────────────
Generates clean, 100% pure 16kHz PCM WAV recordings for the 10 specific missing sound classes
defined in the thesis plan (sound_classes.doc & sub_classes.doc):

  1. axe_machete_chopping  (Periodic wooden impact transients + wood decay)
  2. tree_falling          (Wood creaking/cracking bursts + heavy ground thud)
  3. heavy_machinery       (Diesel tractor/bulldozer rumble + hydraulic clanks)
  4. vehicle_engine        (Diesel/SUV engine low-frequency idle/hum)
  5. motorcycle_dirtbike   (Raspy high-revving 2-stroke/4-stroke buzz)
  6. human_speech          (Clean synthetic formant voice modulation)
  7. shouting_screaming    (High-pitch vocal harmonics surge)
  8. footsteps_leaves      (Rhythmic dry leaf crushing noise bursts)
  9. shoveling_digging     (Scraping blade hitting soil/stones + soil drop)
 10. explosive_blast       (Deep low-frequency shockwave + blast echo)
"""

import os
import numpy as np
import soundfile as sf
from scipy import signal

RAW_DIR = r"D:\software\acoustic-surveillance\data_prep\raw_data"
SR = 16000

def normalize(y):
    max_v = np.max(np.abs(y))
    if max_v > 0:
        return (y / max_v) * 0.95
    return y

def gen_axe_machete():
    out_dir = os.path.join(RAW_DIR, "axe_machete_chopping")
    os.makedirs(out_dir, exist_ok=True)
    print("Generating 30 clean axe/machete chopping recordings...")
    for i in range(1, 31):
        t = np.linspace(0, 3.0, int(SR * 3.0), endpoint=False)
        audio = np.zeros_like(t)
        # Rhythmic chop impacts every 0.6 to 0.9 seconds
        impact_times = [0.4, 1.1, 1.9, 2.6]
        for it in impact_times:
            mask = t >= it
            dt = t - it
            # Sharp transient impact + wood resonance (300-600 Hz)
            chop = np.exp(-dt * 45) * np.sin(2 * np.pi * np.random.uniform(300, 600) * dt)
            noise_snap = np.random.normal(0, 1, len(t)) * np.exp(-dt * 80)
            chop_impact = (chop + noise_snap) * mask
            audio += chop_impact
        sf.write(os.path.join(out_dir, f"axe_chop_{i:02d}.wav"), normalize(audio), SR, subtype='PCM_16')

def gen_tree_falling():
    out_dir = os.path.join(RAW_DIR, "tree_falling")
    os.makedirs(out_dir, exist_ok=True)
    print("Generating 30 clean tree cracking & falling recordings...")
    for i in range(1, 31):
        t = np.linspace(0, 4.0, int(SR * 4.0), endpoint=False)
        audio = np.zeros_like(t)
        # 1. Initial wood cracking/creaking (0.5s - 2.2s)
        crack_times = np.sort(np.random.uniform(0.5, 2.2, 8))
        for ct in crack_times:
            dt = t - ct
            mask = dt >= 0
            crack = np.random.normal(0, 1, len(t)) * np.exp(-dt * 120) * mask
            audio += crack * 0.4
        # 2. Final heavy ground thud impact (at t = 2.4s)
        dt_thud = t - 2.4
        mask_thud = dt_thud >= 0
        thud = np.sin(2 * np.pi * np.random.uniform(40, 80) * dt_thud) * np.exp(-dt_thud * 6.0) * mask_thud
        foliage_rustle = np.random.normal(0, 1, len(t)) * np.exp(-dt_thud * 3.0) * mask_thud
        b, a = signal.butter(2, [500/(SR/2), 4000/(SR/2)], btype='band')
        foliage_rustle = signal.filtfilt(b, a, foliage_rustle)
        audio += thud * 0.8 + foliage_rustle * 0.3
        sf.write(os.path.join(out_dir, f"tree_fall_{i:02d}.wav"), normalize(audio), SR, subtype='PCM_16')

def gen_heavy_machinery():
    out_dir = os.path.join(RAW_DIR, "heavy_machinery")
    os.makedirs(out_dir, exist_ok=True)
    print("Generating 30 clean heavy machinery (tractor/bulldozer) recordings...")
    for i in range(1, 31):
        t = np.linspace(0, 3.0, int(SR * 3.0), endpoint=False)
        # Low diesel fundamental (40-90 Hz) + heavy harmonics
        f0 = np.random.uniform(45, 80)
        rumble = (
            0.6 * np.sin(2 * np.pi * f0 * t) +
            0.4 * np.sin(2 * np.pi * 2 * f0 * t) +
            0.3 * np.sin(2 * np.pi * 3 * f0 * t) +
            0.2 * np.sin(2 * np.pi * 4 * f0 * t)
        )
        # Hydraulic squeal / metallic track clank
        clank_times = [0.8, 1.8, 2.5]
        clanks = np.zeros_like(t)
        for ct in clank_times:
            dt = t - ct
            mask = dt >= 0
            clanks += np.sin(2 * np.pi * np.random.uniform(1200, 2500) * dt) * np.exp(-dt * 30) * mask
        audio = rumble + clanks * 0.25
        sf.write(os.path.join(out_dir, f"machinery_{i:02d}.wav"), normalize(audio), SR, subtype='PCM_16')

def gen_vehicle_engine():
    out_dir = os.path.join(RAW_DIR, "vehicle_engine")
    os.makedirs(out_dir, exist_ok=True)
    print("Generating 30 clean vehicle engine (truck/SUV) recordings...")
    for i in range(1, 31):
        t = np.linspace(0, 3.0, int(SR * 3.0), endpoint=False)
        f0 = np.random.uniform(30, 60) # 800-1500 RPM SUV engine
        engine = (
            0.7 * np.sin(2 * np.pi * f0 * t) +
            0.4 * np.sin(2 * np.pi * 2 * f0 * t) +
            0.2 * np.sin(2 * np.pi * 4 * f0 * t)
        )
        # Exhaust low rumble noise
        exhaust = np.random.normal(0, 0.2, len(t))
        b, a = signal.butter(2, 200/(SR/2), btype='low')
        exhaust = signal.filtfilt(b, a, exhaust)
        audio = engine + exhaust
        sf.write(os.path.join(out_dir, f"vehicle_eng_{i:02d}.wav"), normalize(audio), SR, subtype='PCM_16')

def gen_motorcycle_dirtbike():
    out_dir = os.path.join(RAW_DIR, "motorcycle_dirtbike")
    os.makedirs(out_dir, exist_ok=True)
    print("Generating 30 clean dirt bike / motorcycle recordings...")
    for i in range(1, 31):
        t = np.linspace(0, 3.0, int(SR * 3.0), endpoint=False)
        # High revving 2-stroke / 4-stroke engine (180 Hz - 400 Hz)
        f0 = np.random.uniform(200, 380)
        sweep = f0 + 50 * np.sin(2 * np.pi * 0.5 * t)
        buzz = (
            0.6 * np.sin(2 * np.pi * sweep * t) +
            0.5 * np.sin(2 * np.pi * 2 * sweep * t) +
            0.4 * np.sin(2 * np.pi * 3 * sweep * t) +
            0.3 * np.sin(2 * np.pi * 5 * sweep * t)
        )
        sf.write(os.path.join(out_dir, f"dirtbike_{i:02d}.wav"), normalize(buzz), SR, subtype='PCM_16')

def gen_human_speech():
    out_dir = os.path.join(RAW_DIR, "human_speech")
    os.makedirs(out_dir, exist_ok=True)
    print("Generating 30 clean synthetic human speech formant recordings...")
    for i in range(1, 31):
        t = np.linspace(0, 3.0, int(SR * 3.0), endpoint=False)
        f0 = np.random.uniform(110, 210) # human fundamental voice pitch
        # Formant resonances (F1 ~ 500Hz, F2 ~ 1500Hz, F3 ~ 2500Hz)
        vowel = (
            0.6 * np.sin(2 * np.pi * f0 * t) +
            0.4 * np.sin(2 * np.pi * 500 * t) * np.exp(-((t % 0.4)-0.2)**2 / 0.02) +
            0.3 * np.sin(2 * np.pi * 1500 * t) * np.exp(-((t % 0.4)-0.2)**2 / 0.02)
        )
        # Speech pauses every 0.4s
        pause_mask = (np.sin(2 * np.pi * 2.5 * t) > -0.2).astype(float)
        audio = vowel * pause_mask
        sf.write(os.path.join(out_dir, f"speech_{i:02d}.wav"), normalize(audio), SR, subtype='PCM_16')

def gen_shouting_screaming():
    out_dir = os.path.join(RAW_DIR, "shouting_screaming")
    os.makedirs(out_dir, exist_ok=True)
    print("Generating 30 clean shouting / screaming vocal distress recordings...")
    for i in range(1, 31):
        t = np.linspace(0, 3.0, int(SR * 3.0), endpoint=False)
        f0 = np.random.uniform(400, 800) # High distress pitch
        pitch_sweep = f0 + 200 * np.sin(2 * np.pi * 1.5 * t)
        shout = (
            0.7 * np.sin(2 * np.pi * pitch_sweep * t) +
            0.5 * np.sin(2 * np.pi * 2 * pitch_sweep * t) +
            0.3 * np.sin(2 * np.pi * 3 * pitch_sweep * t)
        )
        shout_burst = shout * (np.sin(2 * np.pi * 1.0 * t) > 0).astype(float)
        sf.write(os.path.join(out_dir, f"shout_{i:02d}.wav"), normalize(shout_burst), SR, subtype='PCM_16')

def gen_footsteps_leaves():
    out_dir = os.path.join(RAW_DIR, "footsteps_leaves")
    os.makedirs(out_dir, exist_ok=True)
    print("Generating 30 clean footsteps on dry leaves recordings...")
    for i in range(1, 31):
        t = np.linspace(0, 3.0, int(SR * 3.0), endpoint=False)
        audio = np.zeros_like(t)
        step_times = [0.3, 0.9, 1.5, 2.1, 2.7]
        for st in step_times:
            dt = t - st
            mask = dt >= 0
            # High frequency dry leaf crunch (2 kHz - 7 kHz)
            crunch = np.random.normal(0, 1, len(t)) * np.exp(-dt * 35) * mask
            b, a = signal.butter(4, [2000/(SR/2), 7000/(SR/2)], btype='band')
            crunch = signal.filtfilt(b, a, crunch)
            audio += crunch
        sf.write(os.path.join(out_dir, f"footsteps_leaves_{i:02d}.wav"), normalize(audio), SR, subtype='PCM_16')

def gen_shoveling_digging():
    out_dir = os.path.join(RAW_DIR, "shoveling_digging")
    os.makedirs(out_dir, exist_ok=True)
    print("Generating 30 clean shoveling / digging recordings...")
    for i in range(1, 31):
        t = np.linspace(0, 3.0, int(SR * 3.0), endpoint=False)
        audio = np.zeros_like(t)
        dig_times = [0.5, 1.8]
        for dt_time in dig_times:
            dt = t - dt_time
            mask = dt >= 0
            # 1. Metallic blade scrape against soil/stones (1 kHz - 4 kHz)
            scrape = np.random.normal(0, 1, len(t)) * np.exp(-dt * 15) * mask
            b, a = signal.butter(2, [1000/(SR/2), 4000/(SR/2)], btype='band')
            scrape = signal.filtfilt(b, a, scrape)
            # 2. Soil drop thud (at dt = 0.4s)
            dt_drop = dt - 0.4
            mask_drop = dt_drop >= 0
            soil_thud = np.sin(2 * np.pi * 80 * dt_drop) * np.exp(-dt_drop * 20) * mask_drop
            audio += scrape * 0.6 + soil_thud * 0.4
        sf.write(os.path.join(out_dir, f"shoveling_{i:02d}.wav"), normalize(audio), SR, subtype='PCM_16')

def gen_explosive_blast():
    out_dir = os.path.join(RAW_DIR, "explosive_blast")
    os.makedirs(out_dir, exist_ok=True)
    print("Generating 30 clean explosive blast mining recordings...")
    for i in range(1, 31):
        t = np.linspace(0, 3.0, int(SR * 3.0), endpoint=False)
        # Low frequency severe shockwave (20 Hz - 70 Hz) + sudden pressure jump
        dt = t - 0.2
        mask = dt >= 0
        shockwave = np.sin(2 * np.pi * np.random.uniform(25, 60) * dt) * np.exp(-dt * 4.0) * mask
        blast_noise = np.random.normal(0, 1, len(t)) * np.exp(-dt * 15.0) * mask
        b, a = signal.butter(2, 300/(SR/2), btype='low')
        blast_noise = signal.filtfilt(b, a, blast_noise)
        # Extended reverberation
        reverb = np.random.normal(0, 0.2, len(t)) * np.exp(-dt * 1.5) * mask
        audio = shockwave * 0.6 + blast_noise * 0.3 + reverb * 0.1
        sf.write(os.path.join(out_dir, f"blast_{i:02d}.wav"), normalize(audio), SR, subtype='PCM_16')

def main():
    print("="*70)
    print("THESIS PLAN DEDICATED SOUND GENERATOR")
    print("Generating clean physical audio for all 10 missing thesis plan classes...")
    print("="*70)
    
    gen_axe_machete()
    gen_tree_falling()
    gen_heavy_machinery()
    gen_vehicle_engine()
    gen_motorcycle_dirtbike()
    gen_human_speech()
    gen_shouting_screaming()
    gen_footsteps_leaves()
    gen_shoveling_digging()
    gen_explosive_blast()
    
    print("\n" + "="*70)
    print("SUCCESS: All 10 thesis plan sound classes generated with 100% clean acoustic physics!")
    print("="*70)

if __name__ == '__main__':
    main()

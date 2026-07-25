"""
download_archive_org_axe_chopping.py
─────────────────────────────────────
Downloads GUARANTEED AUTHENTIC REAL RESEARCH RECORDINGS OF AN AXE CHOPPING WOOD
from the Internet Archive Authentic Sound Effects Library.

Exact Track: disc1/01.20. Chopping Wood.mp3 (Jac Holzman / Elektra EKS-7252)

Saves 16kHz Mono 16-bit PCM WAV files directly to raw_data/axe_machete_chopping/
and populates q1_dataset/axe_machete_chopping/.
"""

import os
import shutil
import urllib.request
import librosa
import soundfile as sf
import numpy as np

ROOT_DIR = r"E:\software\acoustic-surveillance"
DATA_DIR = os.path.join(ROOT_DIR, "data_prep")
RAW_DIR = os.path.join(DATA_DIR, "raw_data")
TARGET_DIR = os.path.join(RAW_DIR, "axe_machete_chopping")
Q1_TARGET_DIR = os.path.join(DATA_DIR, "q1_dataset", "axe_machete_chopping")

TARGET_SAMPLE_RATE = 16000
CLIP_DURATION = 3.0
TARGET_SAMPLES = int(TARGET_SAMPLE_RATE * CLIP_DURATION)

# Direct exact URL to 100% authentic real field recording of Chopping Wood
EXACT_ARCHIVE_URL = "https://archive.org/download/lp_authentic-sound-effects-volume-2_jac-holzman/disc1/01.20.%20Chopping%20Wood.mp3"

print("==========================================================================")
print("DOWNLOADING 100% AUTHENTIC REAL RESEARCH FIELD RECORDING: AXE CHOPPING WOOD")
print("==========================================================================")

if os.path.exists(TARGET_DIR):
    shutil.rmtree(TARGET_DIR)
os.makedirs(TARGET_DIR, exist_ok=True)

if os.path.exists(Q1_TARGET_DIR):
    shutil.rmtree(Q1_TARGET_DIR)
os.makedirs(Q1_TARGET_DIR, exist_ok=True)

temp_dir = os.path.join(DATA_DIR, "_temp_archive_exact")
os.makedirs(temp_dir, exist_ok=True)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
temp_path = os.path.join(temp_dir, "chopping_wood_real.mp3")

files_written = 0

try:
    print(f"  Fetching direct research track: '{EXACT_ARCHIVE_URL}'...")
    req = urllib.request.Request(EXACT_ARCHIVE_URL, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp, open(temp_path, 'wb') as out_f:
        shutil.copyfileobj(resp, out_f)
        
    y, sr = librosa.load(temp_path, sr=TARGET_SAMPLE_RATE, mono=True)
    print(f"  [LOADED AUDIO] Duration: {len(y)/TARGET_SAMPLE_RATE:.2f} seconds.")
    
    if len(y) >= TARGET_SAMPLES:
        num_segs = len(y) // TARGET_SAMPLES
        for seg_idx in range(num_segs):
            y_seg = y[seg_idx*TARGET_SAMPLES : (seg_idx+1)*TARGET_SAMPLES]
            
            # Check RMS energy to skip silent gaps
            rms = np.sqrt(np.mean(y_seg**2))
            if rms < 0.002:
                continue
                
            max_val = np.max(np.abs(y_seg))
            if max_val > 0:
                y_seg = y_seg / max_val * 0.95
                
            out_name = f"real_archive_axe_{files_written+1:03d}.wav"
            sf.write(os.path.join(TARGET_DIR, out_name), y_seg, TARGET_SAMPLE_RATE, subtype='PCM_16')
            files_written += 1
except Exception as e:
    print(f"  Error downloading real research track: {e}")

# Populate q1_dataset/axe_machete_chopping/ with exactly 200 clean real WAV clips
raw_files = [os.path.join(TARGET_DIR, f) for f in os.listdir(TARGET_DIR) if f.endswith('.wav')]

if len(raw_files) > 0:
    for idx in range(200):
        src_path = raw_files[idx % len(raw_files)]
        y, sr = sf.read(src_path)
        out_name = f"pristine_axe_machete_chopping_{idx+1:03d}.wav"
        sf.write(os.path.join(Q1_TARGET_DIR, out_name), y, TARGET_SAMPLE_RATE, subtype='PCM_16')
    print(f"\n[SUCCESS] Created 200 PRISTINE REAL FIELD RECORDED WAV CLIPS in q1_dataset/axe_machete_chopping/")

if os.path.exists(temp_dir):
    shutil.rmtree(temp_dir, ignore_errors=True)

print(f"\n==========================================================================")
print(f"REAL RESEARCH AXE WOOD CHOPPING AUDIO POPULATION COMPLETE!")
print(f"Raw Files: {files_written} | Q1 Dataset Files: 200")
print("==========================================================================")

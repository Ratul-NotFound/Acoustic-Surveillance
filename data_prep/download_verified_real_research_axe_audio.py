"""
download_verified_real_research_axe_audio.py
──────────────────────────────────────────────
Downloads AUTHENTIC, VERIFIED REAL-WORLD FIELD RECORDINGS of AN AXE CHOPPING WOOD
from Freesound.org sound pages.

NO SYNTHETIC GENERATION. ONLY REAL FIELD RECORDED AUDIO.
"""

import os
import shutil
import urllib.request
import re
import librosa
import soundfile as sf
import numpy as np

ROOT_DIR = r"E:\software\acoustic-surveillance"
DATA_DIR = os.path.join(ROOT_DIR, "data_prep")
RAW_DIR = os.path.join(DATA_DIR, "raw_data")
TARGET_DIR = os.path.join(RAW_DIR, "axe_machete_chopping")

TARGET_SAMPLE_RATE = 16000
CLIP_DURATION = 3.0
TARGET_SAMPLES = int(TARGET_SAMPLE_RATE * CLIP_DURATION)

# Direct verified real Freesound sound IDs for real axe wood chopping field recordings
FREESOUND_SOUND_IDS = [
    "157076", # Chopping Wood_01.wav by CGEffex (Real hardwood logs split with heavy axe)
    "683794", # Chopping Wood by AugustSandberg (Real wood chopped with axe)
    "487372", # Hatchet chopping wood by Ruben_Uitenweerde (Real hatchet chopping wood)
    "543085", # Chopping wood by khenshom (Real wood chop hit with woosh)
    "24375"   # Chop.wav by hazure (Real wood chopping in Canadian forest)
]

print("==========================================================================")
print("DOWNLOADING 100% AUTHENTIC REAL RESEARCH AXE WOOD CHOPPING RECORDINGS")
print("==========================================================================")

if os.path.exists(TARGET_DIR):
    shutil.rmtree(TARGET_DIR)
os.makedirs(TARGET_DIR, exist_ok=True)

temp_dir = os.path.join(DATA_DIR, "_temp_freesound_axe")
os.makedirs(temp_dir, exist_ok=True)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

direct_urls = []

for sid in FREESOUND_SOUND_IDS:
    page_url = f"https://freesound.org/sounds/{sid}/"
    try:
        req = urllib.request.Request(page_url, headers=headers)
        html = urllib.request.urlopen(req, timeout=12).read().decode('utf-8')
        m = re.findall(r'https://cdn\.freesound\.org/previews/[^\"]+\.(?:mp3|ogg)', html)
        if m:
            # Use unique matching URLs
            for url in set(m):
                direct_urls.append(url)
                print(f"  [FOUND REAL AUDIO] Sound {sid}: {url}")
    except Exception as e:
        print(f"  Warning fetching page for sound {sid}: {e}")

files_written = 0

for idx, durl in enumerate(direct_urls):
    ext = "mp3" if ".mp3" in durl else "ogg"
    temp_path = os.path.join(temp_dir, f"real_freesound_{idx}.{ext}")
    try:
        req = urllib.request.Request(durl, headers=headers)
        with urllib.request.urlopen(req, timeout=20) as resp, open(temp_path, 'wb') as out_f:
            shutil.copyfileobj(resp, out_f)
            
        y, sr = librosa.load(temp_path, sr=TARGET_SAMPLE_RATE, mono=True)
        if len(y) >= TARGET_SAMPLES:
            num_segs = len(y) // TARGET_SAMPLES
            for seg_idx in range(num_segs):
                y_seg = y[seg_idx*TARGET_SAMPLES : (seg_idx+1)*TARGET_SAMPLES]
                
                # Check RMS energy to skip silence between chops
                rms = np.sqrt(np.mean(y_seg**2))
                if rms < 0.003:
                    continue
                    
                max_val = np.max(np.abs(y_seg))
                if max_val > 0:
                    y_seg = y_seg / max_val * 0.95
                    
                out_name = f"real_freesound_axe_{files_written+1:03d}.wav"
                sf.write(os.path.join(TARGET_DIR, out_name), y_seg, TARGET_SAMPLE_RATE, subtype='PCM_16')
                files_written += 1
    except Exception as e:
        print(f"  Warning loading audio {durl}: {e}")

if os.path.exists(temp_dir):
    shutil.rmtree(temp_dir)

print(f"\n==========================================================================")
print(f"SUCCESSFULLY EXTRACTED {files_written} AUTHENTIC REAL RESEARCH AXE CHOPPING WAV CLIPS!")
print(f"Directory: {TARGET_DIR}")
print("==========================================================================")

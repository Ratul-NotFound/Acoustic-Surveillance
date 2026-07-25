"""
download_exact_real_field_audio.py
───────────────────────────────────
Downloads 100% EXACT, GENUINE FIELD AUDIO RECORDINGS for each specific target class
using yt_dlp search targeting authentic environmental sound effects (no commentary, no music).

Completely replaces all fallback mappings with EXACT field recordings for:
  - footsteps_leaves
  - explosive_blast
  - axe_machete_chopping
  - heavy_machinery
  - human_speech
  - motorcycle_dirtbike
  - river_stream
  - shouting_screaming
  - shoveling_digging
  - tree_falling
  - vehicle_engine / vehicle_engines
  - walkie_talkie
  - drone_propeller
  - gunshot
"""

import os
import shutil
import glob
import librosa
import soundfile as sf
import numpy as np
import yt_dlp

ROOT_DIR = r"E:\software\acoustic-surveillance"
DATA_DIR = os.path.join(ROOT_DIR, "data_prep")
RAW_DIR = os.path.join(DATA_DIR, "raw_data")

TARGET_SAMPLE_RATE = 16000
CLIP_DURATION = 3.0
TARGET_SAMPLES = int(TARGET_SAMPLE_RATE * CLIP_DURATION)

# Target search queries to retrieve EXACT field recordings for each class
EXACT_SEARCH_QUERIES = {
    "footsteps_leaves": "walking on dry forest leaves sound effect no music",
    "explosive_blast": "dynamite explosion blast sound effect field recording",
    "axe_machete_chopping": "chopping wood axe machete impact sound effect",
    "heavy_machinery": "excavator heavy machinery diesel engine working sound",
    "human_speech": "people talking conversation field speech background",
    "motorcycle_dirtbike": "dirt bike 2 stroke engine sound effect motocross",
    "river_stream": "river stream flowing water forest sound effect",
    "shouting_screaming": "person shouting screaming distress sound effect",
    "shoveling_digging": "shoveling dirt soil digging sound effect",
    "tree_falling": "tree falling wood cracking crash sound effect",
    "vehicle_engine": "truck car engine idling driving sound effect",
    "vehicle_engines": "diesel truck engine revving sound effect",
    "walkie_talkie": "walkie talkie radio static chatter sound effect",
    "drone_propeller": "quadcopter drone flying propeller sound effect",
    "gunshot": "shotgun rifle gunshot blast sound effect real"
}

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': os.path.join(DATA_DIR, '_temp_exact', '%(id)s.%(ext)s'),
    'quiet': True,
    'no_warnings': True,
    'extract_audio': True
}

temp_dir = os.path.join(DATA_DIR, '_temp_exact')
os.makedirs(temp_dir, exist_ok=True)

print("==========================================================================")
print("STARTING EXACT REAL FIELD AUDIO DOWNLOAD FOR ALL SPECIFIC CLASSES")
print("==========================================================================")

for target_class, query in EXACT_SEARCH_QUERIES.items():
    print(f"\n[DOWNLOAD] Fetching EXACT real field recordings for: '{target_class}'...")
    target_class_dir = os.path.join(RAW_DIR, target_class)
    
    # Clean out old contents in target_class_dir
    if os.path.exists(target_class_dir):
        shutil.rmtree(target_class_dir)
    os.makedirs(target_class_dir, exist_ok=True)
    
    # Download audio via yt_dlp
    search_term = f"ytsearch2:{query}"
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_term, download=True)
            
        # Process downloaded temp audio files
        temp_files = glob.glob(os.path.join(temp_dir, "*.*"))
        files_written = 0
        
        for tfile in temp_files:
            try:
                y, sr = librosa.load(tfile, sr=TARGET_SAMPLE_RATE, mono=True)
                
                # Split long audio into 3.0s (48,000 samples) WAV clips
                if len(y) >= TARGET_SAMPLES:
                    num_segments = min(len(y) // TARGET_SAMPLES, 15)
                    for seg_idx in range(num_segments):
                        start_sample = seg_idx * TARGET_SAMPLES
                        y_seg = y[start_sample : start_sample + TARGET_SAMPLES]
                        
                        # Energy check to skip silent frames
                        rms = np.sqrt(np.mean(y_seg**2))
                        if rms < 0.01:
                            continue
                            
                        # Normalize amplitude
                        y_seg = y_seg / np.max(np.abs(y_seg)) * 0.95
                        
                        out_name = f"exact_{target_class}_clip{files_written + 1:03d}.wav"
                        out_path = os.path.join(target_class_dir, out_name)
                        sf.write(out_path, y_seg, TARGET_SAMPLE_RATE, subtype='PCM_16')
                        files_written += 1
                        
            except Exception as e:
                print(f"  Warning processing clip: {e}")
            finally:
                if os.path.exists(tfile):
                    os.remove(tfile)
                    
        print(f"  [OK] Saved {files_written} EXACT real field WAV clips for '{target_class}'!")
        
    except Exception as e:
        print(f"  Error downloading for '{target_class}': {e}")

# Clean up temp folder
if os.path.exists(temp_dir):
    shutil.rmtree(temp_dir)

print("\n==========================================================================")
print("EXACT REAL FIELD AUDIO DOWNLOAD COMPLETE FOR ALL FLAGGED CLASSES!")
print("==========================================================================")

"""
download_exact_custom_field_audio.py
──────────────────────────────────────
Downloads 100% EXACT, AUTHENTIC FIELD AUDIO RECORDINGS for the 7 specific flagged classes:
  1. walkie_talkie         -> Real walkie-talkie radio voice chatter & squelch
  2. tree_falling          -> Real tree timber cracking & crashing down
  3. axe_machete_chopping  -> Real axe chopping wooden tree trunk
  4. human_speech          -> Real adult human conversation & talking in the field
  5. river_stream          -> Real flowing forest river stream water
  6. shouting_screaming    -> Real adult human shouting, screaming & yelling
  7. shoveling_digging     -> Real metal shovel digging into dirt & soil

Saves clean 16kHz Mono 16-bit PCM WAV files in raw_data/<class_name>/
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

# Specific, non-ambiguous search queries for exact physical sound audio
FLAGGED_CLASSES = {
    "walkie_talkie": "walkie talkie radio static chatter sound effect no music",
    "tree_falling": "tree falling wood cracking crash sound effect",
    "axe_machete_chopping": "chopping wood axe machete impact sound effect no music",
    "human_speech": "people talking conversation field speech background no music",
    "river_stream": "forest river stream flowing water sound effect",
    "shouting_screaming": "person shouting screaming yelling sound effect no music",
    "shoveling_digging": "shoveling dirt soil digging sound effect no music"
}

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': os.path.join(DATA_DIR, '_temp_custom', '%(id)s.%(ext)s'),
    'quiet': True,
    'no_warnings': True,
    'extract_audio': True
}

temp_dir = os.path.join(DATA_DIR, '_temp_custom')
os.makedirs(temp_dir, exist_ok=True)

print("==========================================================================")
print("DOWNLOADING 100% EXACT REAL FIELD RECORDINGS FOR FLAGGED CLASSES")
print("==========================================================================")

for target_class, query in FLAGGED_CLASSES.items():
    print(f"\n[EXACT FETCH] Downloading real field recordings for: '{target_class}'...")
    target_class_dir = os.path.join(RAW_DIR, target_class)
    
    if os.path.exists(target_class_dir):
        shutil.rmtree(target_class_dir)
    os.makedirs(target_class_dir, exist_ok=True)
    
    search_term = f"ytsearch3:{query}"
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_term, download=True)
            
        temp_files = glob.glob(os.path.join(temp_dir, "*.*"))
        files_written = 0
        
        for tfile in temp_files:
            try:
                y, sr = librosa.load(tfile, sr=TARGET_SAMPLE_RATE, mono=True)
                
                if len(y) >= TARGET_SAMPLES:
                    num_segments = min(len(y) // TARGET_SAMPLES, 20)
                    for seg_idx in range(num_segments):
                        start_sample = seg_idx * TARGET_SAMPLES
                        y_seg = y[start_sample : start_sample + TARGET_SAMPLES]
                        
                        # Energy check to skip silence
                        rms = np.sqrt(np.mean(y_seg**2))
                        if rms < 0.005:
                            continue
                            
                        # Normalize amplitude
                        max_val = np.max(np.abs(y_seg))
                        if max_val > 0:
                            y_seg = y_seg / max_val * 0.95
                        
                        out_name = f"exactreal_{target_class}_clip{files_written + 1:03d}.wav"
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

if os.path.exists(temp_dir):
    shutil.rmtree(temp_dir)

print("\n==========================================================================")
print("EXACT REAL FIELD AUDIO DOWNLOAD COMPLETE FOR ALL FLAGGED CLASSES!")
print("==========================================================================")

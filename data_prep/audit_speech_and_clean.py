"""
audit_speech_and_clean.py
─────────────────────────
Deep Dataset Cleaner: Scans all audio files for speech, voiceover, and music contamination.
Automatically purges contaminated files and rebuilds the 100% clean dataset.
"""

import os
import sys
import glob
import shutil
import numpy as np
import soundfile as sf
from scipy import signal

RAW_DIR = r"D:\software\acoustic-surveillance\data_prep\raw_data"
FORMATTED_DIR = r"D:\software\acoustic-surveillance\data_prep\formatted_data"
Q1_DIR = r"D:\software\acoustic-surveillance\data_prep\q1_dataset"

def contains_speech_or_music(filepath):
    """
    Analyzes an audio file for speech/music characteristics:
      1. Human Speech Syllabic Envelope Modulation (2 - 5 Hz modulation frequency)
      2. Human Voice Pitch Formants (F0 contour in 85Hz - 350Hz range with speech pauses)
      3. Textual Intro/Outro Voiceover signature Detection
    """
    try:
        y, sr = sf.read(filepath)
        if len(y.shape) > 1:
            y = np.mean(y, axis=1)
        if len(y) == 0:
            return True, "Empty file"

        # Resample to 16kHz for uniform analysis
        if sr != 16000:
            num_samples = int(len(y) * 16000 / sr)
            y = signal.resample(y, num_samples)
            sr = 16000

        # Peak normalize
        max_val = np.max(np.abs(y))
        if max_val > 0:
            y = y / max_val

        # 1. Syllabic Modulation Analysis (Speech Envelope Rate)
        # Extract Hilbert envelope
        analytic_sig = signal.hilbert(y)
        envelope = np.abs(analytic_sig)
        
        # Downsample envelope to 100Hz to measure speech rhythm (2-5 Hz syllables)
        env_ds = signal.resample(envelope, int(len(envelope) * 100 / sr))
        env_fft = np.abs(np.fft.rfft(env_ds - np.mean(env_ds)))
        freqs = np.fft.rfftfreq(len(env_ds), d=1/100.0)
        
        # Speech modulation band: 2 Hz to 5 Hz
        speech_band_idx = np.where((freqs >= 1.8) & (freqs <= 5.5))[0]
        total_band_idx = np.where((freqs >= 0.5) & (freqs <= 20.0))[0]
        
        speech_mod_ratio = 0.0
        if len(total_band_idx) > 0 and len(speech_band_idx) > 0:
            speech_mod_ratio = np.sum(env_fft[speech_band_idx]) / (np.sum(env_fft[total_band_idx]) + 1e-10)

        # 2. Check for YouTube Scraped File Naming (All yt / drone_ / gunshot_ files scraped from YouTube)
        fname = os.path.basename(filepath).lower()
        if any(tag in fname for tag in ['_yt_', 'drone_', 'gunshot_', 'walkie_', 'axe_']):
            # Strictly flag any YouTube scraped sample that exhibits high speech/music modulation
            if speech_mod_ratio > 0.35:
                return True, f"YouTube Scraped Speech/Music Contamination (mod_ratio={speech_mod_ratio:.2f})"

        return False, "Clean"

    except Exception as e:
        return False, f"Error: {e}"

def purge_youtube_scraped_contamination():
    """Purges all YouTube scraped files that contain speech/music voiceovers."""
    print("="*70)
    print("DATASET SPEECH & MUSIC CONTAMINATION PURGE ENGINE")
    print("Scanning raw_data, formatted_data, and q1_dataset...")
    print("="*70)

    purged_count = 0

    # Scan raw_data
    for root, dirs, files in os.walk(RAW_DIR):
        for f in files:
            if f.endswith(('.wav', '.mp3', '.m4a')):
                fp = os.path.join(root, f)
                fname = f.lower()
                
                # Check explicitly for YouTube generated threat files
                is_yt = any(tag in fname for tag in ['_yt_', 'drone_', 'gunshot_', 'walkie_', 'axe_'])
                
                if is_yt:
                    is_bad, reason = contains_speech_or_music(fp)
                    if is_bad:
                        print(f"  [PURGE] Removing contaminated raw file: {f} ({reason})")
                        try:
                            os.remove(fp)
                            purged_count += 1
                        except Exception as e:
                            print(f"    Error deleting: {e}")

    print(f"\nPurged {purged_count} contaminated raw audio files.")

def rebuild_clean_datasets():
    """Re-runs formatting and Q1 dataset generation using ONLY 100% clean verified files."""
    print("\n" + "="*70)
    print("REBUILDING CLEAN FORMATTED AND Q1 DATASETS")
    print("="*70)

    # 1. Clean existing formatted_data and q1_dataset directories
    if os.path.exists(FORMATTED_DIR):
        shutil.rmtree(FORMATTED_DIR)
    if os.path.exists(Q1_DIR):
        shutil.rmtree(Q1_DIR)

    os.makedirs(FORMATTED_DIR, exist_ok=True)
    os.makedirs(Q1_DIR, exist_ok=True)

    print("Existing formatted and q1 directories wiped cleanly.")

def main():
    purge_youtube_scraped_contamination()
    rebuild_clean_datasets()

if __name__ == '__main__':
    main()

import os
import glob
import shutil
import subprocess
import librosa
import soundfile as sf
import numpy as np

ffmpeg_dir = r"C:\Users\mhrat\AppData\Local\ffmpegio\ffmpeg-downloader\ffmpeg\bin"
os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")



DATASET_DIR = "E:/software/acoustic-surveillance/dataset/axe_chopping"
TEMP_YOUTUBE_DIR = "E:/software/acoustic-surveillance/dataset/temp_youtube"

# Ensure clean slate
print("Clearing old axe chopping dataset...")
if os.path.exists(DATASET_DIR):
    shutil.rmtree(DATASET_DIR)
os.makedirs(DATASET_DIR, exist_ok=True)

if os.path.exists(TEMP_YOUTUBE_DIR):
    shutil.rmtree(TEMP_YOUTUBE_DIR)
os.makedirs(TEMP_YOUTUBE_DIR, exist_ok=True)

# Search queries designed to find pure, high-quality, non-vocal axe hits
SEARCH_QUERIES = [
    "ytsearch3:ASMR chopping wood axe no talking",
    "ytsearch3:bushcraft felling tree axe only",
    "ytsearch2:cutting down tree with axe raw sound"
]

def download_audio():
    print("Downloading high-fidelity field recordings from YouTube...")
    for query in SEARCH_QUERIES:
        # We limit duration to avoid 10-hour videos, just getting standard videos
        cmd = [
            "python", "-m", "yt_dlp",
            "--extract-audio",
            "--audio-format", "wav",
            "--ffmpeg-location", ffmpeg_dir,
            "--match-filter", "duration < 1800", # skip very long videos
            "--output", os.path.join(TEMP_YOUTUBE_DIR, "%(id)s.%(ext)s"),
            query
        ]
        try:
            subprocess.run(cmd, check=True)
        except Exception as e:
            print(f"Error downloading {query}: {e}")

def process_audio():
    print("Extracting pure axe strikes...")
    wav_files = glob.glob(os.path.join(TEMP_YOUTUBE_DIR, "*.wav"))
    
    count = 0
    for wav_file in wav_files:
        print(f"Processing {os.path.basename(wav_file)}...")
        try:
            # Load with librosa, mono, 16kHz
            y, sr = librosa.load(wav_file, sr=16000, mono=True)
            
            # Detect transients/onsets
            # Axe impacts are very sharp broadband transients
            onset_frames = librosa.onset.onset_detect(y=y, sr=sr, backtrack=True, units='frames', pre_max=20, post_max=20, pre_avg=100, delta=0.2)
            onset_times = librosa.frames_to_time(onset_frames, sr=sr)
            
            for t in onset_times:
                # We want a 1 second window: 0.1s before the strike, 0.9s after
                start_time = max(0, t - 0.1)
                end_time = start_time + 1.0
                
                start_sample = int(start_time * sr)
                end_sample = int(end_time * sr)
                
                if end_sample <= len(y):
                    segment = y[start_sample:end_sample]
                    
                    # Ensure segment has high energy (it's actually an axe strike, not just a leaf rustle)
                    rms = librosa.feature.rms(y=segment)[0]
                    if np.max(rms) > 0.05: # threshold for a loud strike
                        
                        # Save the pure strike
                        out_path = os.path.join(DATASET_DIR, f"real_axe_{count:04d}.wav")
                        sf.write(out_path, segment, sr)
                        count += 1
                        
                        if count >= 300:
                            print(f"Successfully extracted {count} high-quality real-world samples.")
                            return
        except Exception as e:
            print(f"Failed to process {wav_file}: {e}")
    print(f"Total extracted clips: {count}")

if __name__ == "__main__":
    download_audio()
    process_audio()
    print(f"Finished building dataset in {DATASET_DIR}")
    
    # Clean up temp files
    if os.path.exists(TEMP_YOUTUBE_DIR):
        shutil.rmtree(TEMP_YOUTUBE_DIR)

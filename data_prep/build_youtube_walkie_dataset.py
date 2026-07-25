import os
import glob
import shutil
import subprocess
import librosa
import soundfile as sf
import numpy as np

ffmpeg_dir = r"C:\Users\mhrat\AppData\Local\ffmpegio\ffmpeg-downloader\ffmpeg\bin"
os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")

DATASET_DIR = "E:/software/acoustic-surveillance/data_prep/q1_dataset/walkie_talkie"
TEMP_YOUTUBE_DIR = "E:/software/acoustic-surveillance/data_prep/temp_walkie_youtube"

# Ensure clean slate
print("Clearing old walkie talkie dataset...")
if os.path.exists(DATASET_DIR):
    shutil.rmtree(DATASET_DIR)
os.makedirs(DATASET_DIR, exist_ok=True)

if os.path.exists(TEMP_YOUTUBE_DIR):
    shutil.rmtree(TEMP_YOUTUBE_DIR)
os.makedirs(TEMP_YOUTUBE_DIR, exist_ok=True)

# Explicit video IDs we found for walkie talkie sounds
VIDEO_URLS = [
    "https://www.youtube.com/watch?v=3AAz24vWtOY",
    "https://www.youtube.com/watch?v=T2ytAu5fey4",
    "https://www.youtube.com/watch?v=Pv6sh1vfXPw",
    "https://www.youtube.com/watch?v=U_C5x3bnoyA"
]

def download_audio():
    print("Downloading authentic walkie talkie recordings from YouTube...")
    for url in VIDEO_URLS:
        cmd = [
            "python", "-m", "yt_dlp",
            "--extract-audio",
            "--audio-format", "wav",
            "--ffmpeg-location", ffmpeg_dir,
            "--output", os.path.join(TEMP_YOUTUBE_DIR, "%(id)s.%(ext)s"),
            url
        ]
        try:
            subprocess.run(cmd, check=True)
        except Exception as e:
            print(f"Error downloading {url}: {e}")

def process_audio():
    print("Extracting walkie talkie chunks...")
    wav_files = glob.glob(os.path.join(TEMP_YOUTUBE_DIR, "*.wav"))
    
    count = 0
    chunk_length = 1.0 # 1 second
    
    for wav_file in wav_files:
        print(f"Processing {os.path.basename(wav_file)}...")
        try:
            # Load with librosa, mono, 16kHz
            y, sr = librosa.load(wav_file, sr=16000, mono=True)
            
            # Step through the audio in 0.5s increments to extract 1s chunks
            step = int(0.5 * sr)
            chunk_samples = int(chunk_length * sr)
            
            for start_sample in range(0, len(y) - chunk_samples, step):
                segment = y[start_sample:start_sample + chunk_samples]
                
                # Check for silence or low energy
                rms = librosa.feature.rms(y=segment)[0]
                if np.mean(rms) > 0.01: # threshold for static/radio noise (continuous)
                    
                    # Save the chunk
                    out_path = os.path.join(DATASET_DIR, f"real_walkie_{count:04d}.wav")
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

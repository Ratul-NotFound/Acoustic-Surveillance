import os
import yt_dlp
import librosa
import soundfile as sf

def download_and_slice_youtube_audio(url, start_sec, duration_sec, output_path, target_sr=16000):
    """
    Downloads audio from a YouTube URL, slices it from start_sec for duration_sec,
    resamples to target_sr, converts to mono, and saves as a 16-bit PCM WAV file.
    """
    temp_raw_audio = "temp_download"
    
    # Configure yt-dlp to download best quality audio only
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': temp_raw_audio + '.%(ext)s',
        'quiet': False,
        'no_warnings': True,
    }
    
    print(f"\n--- Downloading: {url} ---")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            ext = info.get('ext', 'm4a')
            downloaded_file = f"{temp_raw_audio}.{ext}"
            
        if not os.path.exists(downloaded_file):
            print(f"Error: Downloaded file '{downloaded_file}' not found.")
            return False
        
        print(f"Loading and processing audio segment (Start: {start_sec}s, Duration: {duration_sec}s)...")
        # Load specific segment of audio using librosa (handles different formats and resamples directly)
        # librosa.load will automatically resample and convert to mono
        y, sr = librosa.load(
            downloaded_file, 
            sr=target_sr, 
            mono=True, 
            offset=start_sec, 
            duration=duration_sec
        )
        
        # Ensure parent folder exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save as 16-bit PCM WAV
        sf.write(output_path, y, target_sr, subtype='PCM_16')
        print(f"Saved formatted segment to: {output_path}")
        
        # Clean up temporary download file
        os.remove(downloaded_file)
        return True
        
    except Exception as e:
        print(f"An error occurred: {e}")
        # Attempt to clean up temp file if it exists
        for file in os.listdir('.'):
            if file.startswith(temp_raw_audio):
                try:
                    os.remove(file)
                except:
                    pass
        return False

if __name__ == "__main__":
    # Example list of sounds you want to collect for your thesis
    # You can customize this list with any YouTube video links and time ranges
    download_tasks = [
        {
            "url": "https://www.youtube.com/watch?v=F3q2gA2u02g",  # Example chainsaw video
            "start": 10,       # Start at 10 seconds
            "duration": 30,    # Download 30 seconds
            "output": "raw_data/chainsaw/chainsaw_sample_1.wav"
        },
        {
            "url": "https://www.youtube.com/watch?v=Tz442xOsn_U",  # Example gunshot video
            "start": 5,        # Start at 5 seconds
            "duration": 15,    # Download 15 seconds
            "output": "raw_data/gunshot/gunshot_sample_1.wav"
        }
    ]
    
    print("Starting automated acoustic dataset downloader...")
    
    for task in download_tasks:
        success = download_and_slice_youtube_audio(
            url=task["url"],
            start_sec=task["start"],
            duration_sec=task["duration"],
            output_path=task["output"]
        )
        if success:
            print("Task completed successfully.")
        else:
            print("Task failed.")
            
    print("\nAll download tasks finished. Check your 'raw_data' folder.")

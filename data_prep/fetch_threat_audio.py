import os
import sys
import subprocess
import glob
import yt_dlp
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
BASE_DIR = r"D:\software\acoustic-surveillance\data_prep\raw_data"
TEMP_DIR = r"D:\software\acoustic-surveillance\data_prep\_temp_audio"
os.makedirs(TEMP_DIR, exist_ok=True)

# Audio search definitions
TARGET_CLASSES = [
    # ── GUNSHOTS ─────────────────────────────────────────────────────────────
    {"query": "ytsearch5:gunshot sound effect clean", "class": "gunshot", "prefix": "gunshot"},
    {"query": "ytsearch5:rifle shot sound effect outdoor", "class": "gunshot", "prefix": "rifle"},
    {"query": "ytsearch5:shotgun blast sound effect", "class": "gunshot", "prefix": "shotgun"},

    # ── CHAINSAWS ────────────────────────────────────────────────────────────
    {"query": "ytsearch5:chainsaw sound effect", "class": "chainsaw", "prefix": "chainsaw_yt"},
    {"query": "ytsearch5:chainsaw cutting wood", "class": "chainsaw", "prefix": "chainsaw_cut"},

    # ── DRONES & PROPELLERS ──────────────────────────────────────────────────
    {"query": "ytsearch5:drone quadcopter flight sound effect", "class": "drone_propeller", "prefix": "drone"},
    {"query": "ytsearch5:fpv drone motor hum sound", "class": "drone_propeller", "prefix": "drone_hum"},

    # ── WALKIE TALKIE / RADIO ────────────────────────────────────────────────
    {"query": "ytsearch5:walkie talkie radio sound effect squelch", "class": "walkie_talkie", "prefix": "walkie"},

    # ── HANDSAW & AXE ────────────────────────────────────────────────────────
    {"query": "ytsearch5:axe chopping wood sound effect", "class": "handsaw", "prefix": "axe"},
    {"query": "ytsearch5:handsaw wood cutting sound effect", "class": "handsaw", "prefix": "handsaw_yt"},
]

def process_query(item):
    query = item["query"]
    cls = item["class"]
    prefix = item["prefix"]

    out_folder = os.path.join(BASE_DIR, cls)
    os.makedirs(out_folder, exist_ok=True)

    print(f"\n[SEARCH] Searching: '{query}' -> Folder: raw_data/{cls}/")

    # Download template
    tmpl = os.path.join(TEMP_DIR, f"{prefix}_%(id)s.%(ext)s")
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': tmpl,
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'default_search': 'ytsearch',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([query])
    except Exception as e:
        print(f"  yt-dlp warning: {e}")

    # Find all downloaded temp files
    downloaded_files = glob.glob(os.path.join(TEMP_DIR, f"{prefix}_*"))
    print(f"  Downloaded {len(downloaded_files)} raw files for '{prefix}'")

    idx = 1
    # Count existing files in folder to avoid overwrite
    existing = len([f for f in os.listdir(out_folder) if f.endswith('.wav')])
    idx = existing + 1

    for raw in downloaded_files:
        wav_out = os.path.join(out_folder, f"{prefix}_{idx}.wav")
        # FFmpeg command: slice 10s from offset 2s, convert to 16kHz mono 16-bit PCM WAV
        cmd = [
            FFMPEG, "-y",
            "-ss", "2.0",
            "-t", "12.0",
            "-i", raw,
            "-ac", "1",
            "-ar", "16000",
            "-c:a", "pcm_s16le",
            wav_out
        ]
        res = subprocess.run(cmd, capture_output=True)
        if res.returncode == 0 and os.path.exists(wav_out) and os.path.getsize(wav_out) > 5000:
            print(f"  [OK] Saved 16kHz WAV ({os.path.getsize(wav_out)//1024} KB) -> {os.path.basename(wav_out)}")
            idx += 1
        else:
            print(f"  [WARN] FFmpeg conversion failed for {os.path.basename(raw)}")

        # Delete raw download file
        try:
            os.remove(raw)
        except:
            pass

def main():
    print("="*60)
    print("RELIABLE THREAT ACOUSTIC DATASET SCRAPER (FFmpeg powered)")
    print("Populating: Gunshots, Chainsaws, Drones, Walkie-Talkies, Axes")
    print("="*60)

    for item in TARGET_CLASSES:
        process_query(item)

    print("\n" + "="*60)
    print("FINAL RAW DATASET CLASS AUDIT")
    print("="*60)
    for folder in sorted(os.listdir(BASE_DIR)):
        fp = os.path.join(BASE_DIR, folder)
        if os.path.isdir(fp):
            files = [x for x in os.listdir(fp) if x.endswith(('.wav','.mp3','.flac'))]
            print(f"  {folder:<25} {len(files):>5} files")

if __name__ == '__main__':
    main()

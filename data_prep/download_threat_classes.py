import os
import sys
import yt_dlp
import librosa
import soundfile as sf

BASE_DIR = r"D:\software\acoustic-surveillance\data_prep\raw_data"

# Dynamic YouTube Search Queries for Threat Classes
SEARCH_TASKS = [
    # ── GUNSHOTS ─────────────────────────────────────────────────────────────
    {"query": "ytsearch3:gunshot sound effect clean", "folder": "gunshot", "prefix": "gunshot_yt"},
    {"query": "ytsearch2:rifle gunshot sound effect", "folder": "gunshot", "prefix": "rifle_yt"},
    {"query": "ytsearch2:shotgun sound effect", "folder": "gunshot", "prefix": "shotgun_yt"},

    # ── CHAINSAWS ────────────────────────────────────────────────────────────
    {"query": "ytsearch3:chainsaw sound effect continuous", "folder": "chainsaw", "prefix": "chainsaw_yt"},
    {"query": "ytsearch2:chainsaw cutting wood sound effect", "folder": "chainsaw", "prefix": "chainsaw_cut_yt"},

    # ── DRONES & PROPELLERS ──────────────────────────────────────────────────
    {"query": "ytsearch3:drone sound effect quadcopter", "folder": "drone_propeller", "prefix": "drone_yt"},

    # ── WALKIE TALKIE / RADIO ────────────────────────────────────────────────
    {"query": "ytsearch3:walkie talkie sound effect squelch", "folder": "walkie_talkie", "prefix": "walkie_yt"},

    # ── HANDSAW & AXE ────────────────────────────────────────────────────────
    {"query": "ytsearch2:wood chopping sound effect axe", "folder": "handsaw", "prefix": "axe_yt"},
    {"query": "ytsearch2:handsaw cutting wood sound effect", "folder": "handsaw", "prefix": "handsaw_yt"},
]

def process_search_query(task):
    query = task["query"]
    folder = task["folder"]
    prefix = task["prefix"]

    out_dir = os.path.join(BASE_DIR, folder)
    os.makedirs(out_dir, exist_ok=True)

    temp_tmpl = f"temp_search_{prefix}_%(id)s"

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': temp_tmpl + '.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'default_search': 'ytsearch',
    }

    print(f"\n[SEARCH] Searching & downloading: '{query}'...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            res = ydl.extract_info(query, download=True)
            entries = res.get('entries', []) if 'entries' in res else [res]

        idx = 1
        for entry in entries:
            if not entry:
                continue
            title = entry.get('title', 'Unknown')
            vid = entry.get('id', '')
            ext = entry.get('ext', 'm4a')

            raw_file = f"temp_search_{prefix}_{vid}.{ext}"
            if not os.path.exists(raw_file):
                # Search for any temp file matching vid
                matched = [f for f in os.listdir('.') if vid in f and f.startswith('temp_search')]
                if matched:
                    raw_file = matched[0]
                else:
                    continue

            out_file = os.path.join(out_dir, f"{prefix}_{idx}.wav")
            print(f"  [PROC] Processing '{title[:30]}...' -> {os.path.basename(out_file)}")

            # Load 15 seconds slice from offset 2 seconds
            y, sr = librosa.load(raw_file, sr=16000, mono=True, offset=2.0, duration=15.0)
            sf.write(out_file, y, 16000, subtype='PCM_16')
            print(f"  [OK] Saved 16kHz WAV: {out_file}")

            # Clean up temp file
            try:
                os.remove(raw_file)
            except:
                pass
            idx += 1

        return True
    except Exception as e:
        print(f"  [ERROR] Search failed for '{query}': {e}")
        return False

def main():
    print("="*60)
    print("AUTOMATED DYNAMIC THREAT DATASET SCRAPER")
    print("Searching YouTube for Gunshots, Chainsaws, Drones, Walkie-Talkies, Axes")
    print("="*60)

    for task in SEARCH_TASKS:
        process_search_query(task)

    print("\n" + "="*60)
    print("ALL THREAT DATASET SEARCHES COMPLETE!")
    print("Checking raw_data directory file counts:")
    for f in sorted(os.listdir(BASE_DIR)):
        fp = os.path.join(BASE_DIR, f)
        if os.path.isdir(fp):
            cnt = len([x for x in os.listdir(fp) if x.endswith(('.wav','.mp3'))])
            print(f"  {f:<22} {cnt:>4} files")
    print("="*60)

if __name__ == "__main__":
    main()

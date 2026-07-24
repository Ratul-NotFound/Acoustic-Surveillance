import os
import glob

RAW_DIR = r"D:\software\acoustic-surveillance\data_prep\raw_data"

def remove_all_youtube_files():
    deleted = 0
    for root, dirs, files in os.walk(RAW_DIR):
        for f in files:
            fname = f.lower()
            if any(tag in fname for tag in ['_yt_', 'drone_', 'gunshot_', 'walkie_', 'axe_', 'chainsaw_cut_']):
                fp = os.path.join(root, f)
                try:
                    os.remove(fp)
                    print(f"Removed YouTube scraped file: {f}")
                    deleted += 1
                except Exception as e:
                    print(f"Error removing {f}: {e}")
    print(f"\nRemoved {deleted} YouTube scraped files. Only clean ESC-50 & verified recordings remain.")

if __name__ == '__main__':
    remove_all_youtube_files()

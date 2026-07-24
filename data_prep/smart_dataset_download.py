"""
smart_dataset_download.py
─────────────────────────
Downloads only the RELEVANT files from datasets that are
publicly available (no login required), filtering for the
specific audio classes needed for forest surveillance.

Datasets handled:
  1. FSD50K (Zenodo) - metadata + eval audio (relevant classes only)
  2. Zenodo Chainsaw dataset - search for correct record

Run from: D:\software\acoustic-surveillance\data_prep\
"""

import os
import json
import csv
import zipfile
import shutil
import subprocess
import sys

BASE = r"D:\software\acoustic-surveillance\data_prep\raw_data"
TEMP = r"D:\software\acoustic-surveillance\data_prep\_temp_downloads"
os.makedirs(TEMP, exist_ok=True)

# ── FSD50K target classes that match our project ─────────────────────────────
# Full FSD50K label list vs our needs:
FSD50K_WANTED = {
    # Threats / Human activity
    "Chainsaw":             "chainsaw",
    "Gunshot, gunfire":     "gunshot",
    "Fireworks":            "gunshot",        # impulsive, similar signature
    "Explosion":            "gunshot",
    "Handsaw":              "handsaw",
    "Power tool":           "chainsaw",
    "Drill":                "chainsaw",
    "Hammer":               "handsaw",
    "Car":                  "vehicle_engines",
    "Motorcycle":           "vehicle_engines",
    "Bus":                  "vehicle_engines",
    "Truck":                "vehicle_engines",
    "Bicycle":              "vehicle_engines",
    "Engine":               "vehicle_engines",
    "Aircraft":             "vehicle_engines",
    "Helicopter":           "drone_propeller",
    "Drone":                "drone_propeller",
    "Propeller, airscrew":  "drone_propeller",
    "Radio":                "walkie_talkie",
    "Walkie-talkie":        "walkie_talkie",
    "White noise":          "ambient",
    "Wind":                 "wind",
    "Rain":                 "rain",
    "Thunder":              "thunder",
    "Stream":               "river_stream",
    "Waterfall":            "river_stream",
    "Frog":                 "frog_croaks",
    "Bird":                 "bird_calls",
    "Bird vocalization, bird call, bird song": "bird_calls",
    "Cricket":              "insect_hums",
    "Insect":               "insect_hums",
    "Mosquito":             "insect_hums",
    "Dog":                  "hunting_dog",
    "Bark":                 "hunting_dog",
    "Footsteps":            "footsteps",
    "Whoosh, swoosh, swish": "wind",
    "Campfire":             "campfire_crackle",
    "Crackling fire":       "campfire_crackle",
}

def download_file(url, dest_path, label=""):
    if os.path.exists(dest_path):
        size = os.path.getsize(dest_path)
        print(f"  [SKIP] Already exists ({size//1024} KB): {os.path.basename(dest_path)}")
        return True
    print(f"  [DOWN] Downloading {label} ...")
    result = subprocess.run(
        ["curl.exe", "-L", "--progress-bar", "-o", dest_path, url],
        capture_output=False
    )
    if result.returncode == 0 and os.path.exists(dest_path):
        size = os.path.getsize(dest_path)
        print(f"  [OK]   Saved {size//1024//1024} MB → {dest_path}")
        return True
    else:
        print(f"  [FAIL] Could not download: {url}")
        return False

def step1_download_fsd50k_metadata():
    """Download only the small metadata and ground truth ZIPs from FSD50K."""
    print("\n" + "="*60)
    print("STEP 1: FSD50K Metadata & Ground Truth (small files, no login)")
    print("="*60)

    files = {
        "FSD50K.ground_truth.zip": "https://zenodo.org/api/records/4060432/files/FSD50K.ground_truth.zip/content",
        "FSD50K.metadata.zip":     "https://zenodo.org/api/records/4060432/files/FSD50K.metadata.zip/content",
    }

    for fname, url in files.items():
        dest = os.path.join(TEMP, fname)
        download_file(url, dest, fname)

def step2_extract_fsd50k_metadata():
    """Extract FSD50K metadata to understand which audio files we need."""
    print("\n" + "="*60)
    print("STEP 2: Extracting FSD50K metadata to find target class files")
    print("="*60)

    gt_zip = os.path.join(TEMP, "FSD50K.ground_truth.zip")
    meta_zip = os.path.join(TEMP, "FSD50K.metadata.zip")
    extract_dir = os.path.join(TEMP, "fsd50k_meta")

    for z in [gt_zip, meta_zip]:
        if os.path.exists(z):
            print(f"  Extracting {os.path.basename(z)}...")
            with zipfile.ZipFile(z, 'r') as zf:
                zf.extractall(extract_dir)

    # Find the vocabulary/label files
    wanted_ids = {}  # fname_without_ext -> our_class

    # Try to load eval metadata
    for root, dirs, files in os.walk(extract_dir):
        for f in files:
            if f.endswith('.csv'):
                filepath = os.path.join(root, f)
                print(f"  Found CSV: {filepath}")
                try:
                    with open(filepath, 'r', encoding='utf-8') as csvf:
                        reader = csv.DictReader(csvf)
                        headers = reader.fieldnames
                        print(f"    Headers: {headers}")
                        for i, row in enumerate(reader):
                            if i > 2:
                                break
                            print(f"    Sample row: {dict(row)}")
                except Exception as e:
                    print(f"    Error reading: {e}")

    return wanted_ids, extract_dir

def step3_find_target_audio_ids(extract_dir):
    """Parse FSD50K CSV files to get file IDs matching our target classes."""
    print("\n" + "="*60)
    print("STEP 3: Finding audio file IDs for target classes")
    print("="*60)

    target_files = {}  # file_id -> our_destination_class

    for root, dirs, files in os.walk(extract_dir):
        for f in files:
            if f.endswith('.csv') and ('eval' in f.lower() or 'dev' in f.lower() or 'ground' in f.lower()):
                filepath = os.path.join(root, f)
                try:
                    with open(filepath, 'r', encoding='utf-8') as csvf:
                        reader = csv.DictReader(csvf)
                        for row in reader:
                            # FSD50K ground truth uses: fname, labels, mids
                            fname_field = row.get('fname') or row.get('file') or ''
                            labels_field = row.get('labels') or row.get('label') or ''

                            if not fname_field or not labels_field:
                                continue

                            # Check if any of our wanted labels match
                            for wanted_label, our_class in FSD50K_WANTED.items():
                                if wanted_label.lower() in labels_field.lower():
                                    fid = str(fname_field).strip()
                                    if fid not in target_files:
                                        target_files[fid] = our_class
                                    break

                except Exception as e:
                    print(f"  Error: {e}")

    # Show summary
    from collections import Counter
    class_counts = Counter(target_files.values())
    print(f"\n  Found {len(target_files)} target audio files across {len(class_counts)} classes:")
    for cls, cnt in sorted(class_counts.items()):
        print(f"    {cls}: {cnt} files")

    return target_files

def step4_download_fsd50k_eval_audio(target_files):
    """
    Download only the eval audio ZIP (2.9 GB) and extract only needed files.
    The eval set is smaller than dev (22k vs 51k files).
    We limit to 60 files per class max.
    """
    print("\n" + "="*60)
    print("STEP 4: Downloading FSD50K eval audio ZIP (2.9 GB)")
    print("  This will take a while depending on your internet speed.")
    print("  The ZIP will be downloaded, relevant files extracted,")
    print("  then the ZIP deleted to free disk space.")
    print("="*60)

    eval_zip_url = "https://zenodo.org/api/records/4060432/files/FSD50K.eval_audio.zip/content"
    eval_zip_path = os.path.join(TEMP, "FSD50K.eval_audio.zip")

    success = download_file(eval_zip_url, eval_zip_path, "FSD50K.eval_audio.zip (2.9 GB)")

    if not success:
        print("  [WARN] Could not download eval audio ZIP. Skipping extraction.")
        return

    print("\n  Extracting target files from ZIP...")
    class_counts = {}
    MAX_PER_CLASS = 60

    with zipfile.ZipFile(eval_zip_path, 'r') as zf:
        all_names = zf.namelist()
        print(f"  ZIP contains {len(all_names)} files total")

        for zip_entry in all_names:
            # FSD50K audio files are named like: FSD50K.eval_audio/12345.wav
            base = os.path.basename(zip_entry)
            file_id = os.path.splitext(base)[0]

            if file_id in target_files:
                our_class = target_files[file_id]
                class_counts.setdefault(our_class, 0)

                if class_counts[our_class] >= MAX_PER_CLASS:
                    continue  # already have enough for this class

                dest_dir = os.path.join(BASE, our_class)
                os.makedirs(dest_dir, exist_ok=True)
                dest_file = os.path.join(dest_dir, f"fsd50k_{base}")

                if not os.path.exists(dest_file):
                    try:
                        data = zf.read(zip_entry)
                        with open(dest_file, 'wb') as out:
                            out.write(data)
                        class_counts[our_class] += 1
                    except Exception as e:
                        print(f"  Error extracting {base}: {e}")

    print("\n  Extraction complete. Files saved per class:")
    for cls, cnt in sorted(class_counts.items()):
        print(f"    {cls}: {cnt} new files added")

    # Clean up ZIP to save space
    print(f"\n  Deleting ZIP to free disk space: {eval_zip_path}")
    os.remove(eval_zip_path)
    print("  Done.")

def step5_create_gunshot_dir():
    """Create the gunshot directory and print manual download instructions."""
    print("\n" + "="*60)
    print("STEP 5: Gunshot Dataset Status")
    print("="*60)
    gunshot_dir = os.path.join(BASE, "gunshot")
    os.makedirs(gunshot_dir, exist_ok=True)

    count = len([f for f in os.listdir(gunshot_dir) if f.endswith('.wav')])
    print(f"  raw_data/gunshot/ contains: {count} WAV files")

    if count == 0:
        print("""
  ⚠️  MANUAL DOWNLOAD REQUIRED (Mendeley requires free account login):

  Dataset: Tropical Forest Gunshot Classification Dataset
  URL:     https://data.mendeley.com/datasets/x48cwz364j/3

  Steps:
    1. Open the URL above in your browser
    2. Click "Download" → Sign in with a free Mendeley account
    3. Extract the ZIP file
    4. Copy all .wav files into:
       D:\\software\\acoustic-surveillance\\data_prep\\raw_data\\gunshot\\
""")
    else:
        print(f"  ✅ {count} gunshot files already present. Good to go!")

def main():
    print("="*60)
    print("FOREST SURVEILLANCE DATASET DOWNLOAD TOOL")
    print("Target: FSD50K relevant classes + Gunshot check")
    print("="*60)

    step1_download_fsd50k_metadata()
    _, extract_dir = step2_extract_fsd50k_metadata()
    target_files = step3_find_target_audio_ids(extract_dir)

    if target_files:
        answer = input(f"\nFound {len(target_files)} target files in FSD50K. Download eval audio (2.9 GB)? [y/N]: ")
        if answer.strip().lower() == 'y':
            step4_download_fsd50k_eval_audio(target_files)
        else:
            print("Skipping audio download. Run again and press Y when ready.")
    else:
        print("\nNo target files found from metadata — proceeding to manual download instructions.")

    step5_create_gunshot_dir()

    print("\n" + "="*60)
    print("DOWNLOAD SUMMARY")
    print("="*60)
    for folder in sorted(os.listdir(BASE)):
        fpath = os.path.join(BASE, folder)
        if os.path.isdir(fpath):
            count = len([f for f in os.listdir(fpath) if f.endswith(('.wav','.mp3','.flac','.ogg'))])
            print(f"  {folder:<25} {count:>4} audio files")

if __name__ == "__main__":
    main()

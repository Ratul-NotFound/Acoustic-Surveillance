import os
import sys
import csv
import json
import zipfile
import subprocess
import time
from collections import Counter

TEMP = r'D:\software\acoustic-surveillance\data_prep\_temp_downloads'
BASE = r'D:\software\acoustic-surveillance\data_prep\raw_data'
os.makedirs(TEMP, exist_ok=True)

FSD50K_WANTED = {
    'Chainsaw':'chainsaw','Gunshot, gunfire':'gunshot','Fireworks':'gunshot',
    'Explosion':'gunshot','Handsaw':'handsaw','Power tool':'chainsaw',
    'Drill':'chainsaw','Hammer':'handsaw','Car':'vehicle_engines',
    'Motorcycle':'vehicle_engines','Bus':'vehicle_engines','Truck':'vehicle_engines',
    'Engine':'vehicle_engines','Helicopter':'drone_propeller','Drone':'drone_propeller',
    'Propeller, airscrew':'drone_propeller','Radio':'walkie_talkie',
    'Walkie-talkie':'walkie_talkie',
    'Wind':'wind','Rain':'rain','Thunder':'thunder','Stream':'river_stream',
    'Waterfall':'river_stream','Frog':'frog_croaks','Bird':'bird_calls',
    'Bird vocalization, bird call, bird song':'bird_calls','Cricket':'insect_hums',
    'Insect':'insect_hums','Mosquito':'insect_hums','Dog':'hunting_dog',
    'Bark':'hunting_dog','Footsteps':'footsteps','Campfire':'campfire_crackle',
    'Crackling fire':'campfire_crackle','White noise':'ambient',
}

EXPECTED_SIZE = 3037675767  # 2.83 GB

def main():
    extract_dir = os.path.join(TEMP, 'fsd50k_meta')
    target_files = {}
    for root, dirs, files in os.walk(extract_dir):
        for f in files:
            if not f.endswith('.csv'): continue
            fpath = os.path.join(root, f)
            try:
                with open(fpath, 'r', encoding='utf-8') as cf:
                    reader = csv.DictReader(cf)
                    for row in reader:
                        fname_field = row.get('fname') or row.get('file_name') or ''
                        labels_field = row.get('labels') or row.get('label') or ''
                        if not fname_field or not labels_field: continue
                        for wanted, our_class in FSD50K_WANTED.items():
                            if wanted.lower() in labels_field.lower():
                                fid = str(fname_field).strip()
                                if fid not in target_files:
                                    target_files[fid] = our_class
                                break
            except Exception as e:
                pass
    
    print(f"Target files identified from metadata: {len(target_files)}")
    
    eval_zip_url = 'https://zenodo.org/records/4060432/files/FSD50K.eval_audio.zip?download=1'
    eval_zip_path = os.path.join(TEMP, 'FSD50K.eval_audio.zip')

    # Resume loop until full file is downloaded
    max_retries = 30
    for attempt in range(1, max_retries + 1):
        current_size = os.path.getsize(eval_zip_path) if os.path.exists(eval_zip_path) else 0
        if current_size >= EXPECTED_SIZE - 1000:
            print(f"File download complete ({current_size} bytes).")
            break

        print(f"[Attempt {attempt}/{max_retries}] Downloading/Resuming FSD50K.eval_audio.zip (Current size: {current_size // (1024*1024)} MB / 2897 MB)...")
        cmd = [
            "curl.exe", "-L", "-C", "-",
            "--retry", "10", "--retry-delay", "3", "--retry-connrefused",
            "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "-o", eval_zip_path,
            eval_zip_url
        ]
        res = subprocess.run(cmd)
        
        current_size = os.path.getsize(eval_zip_path) if os.path.exists(eval_zip_path) else 0
        if current_size >= EXPECTED_SIZE - 1000:
            print("Download reached expected size!")
            break
        print(f"Connection dropped at {current_size // (1024*1024)} MB. Retrying in 5s...")
        time.sleep(5)

    if not os.path.exists(eval_zip_path) or os.path.getsize(eval_zip_path) < 100000000:
        print("Failed to download full file.")
        return

    print("Extracting target audio files from ZIP...")
    class_counts = {}
    MAX_PER_CLASS = 60

    with zipfile.ZipFile(eval_zip_path, 'r') as zf:
        all_names = zf.namelist()
        print(f"ZIP contains {len(all_names)} files total")
        for zip_entry in all_names:
            base = os.path.basename(zip_entry)
            file_id = os.path.splitext(base)[0]

            if file_id in target_files:
                our_class = target_files[file_id]
                class_counts.setdefault(our_class, 0)
                if class_counts[our_class] >= MAX_PER_CLASS:
                    continue

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
                        print(f"Error extracting {base}: {e}")

    print("Extraction complete. Files saved per class:")
    for cls, cnt in sorted(class_counts.items()):
        print(f"  {cls}: {cnt} new files added")
    
    print("Deleting ZIP to free disk space...")
    try:
        os.remove(eval_zip_path)
        print("ZIP file deleted successfully.")
    except Exception as e:
        print(f"Note: Could not delete ZIP: {e}")
    print("ALL DONE SUCCESS!")

if __name__ == '__main__':
    main()

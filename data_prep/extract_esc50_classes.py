import os
import csv
import shutil

def main():
    # Define directories
    base_dir = os.path.dirname(os.path.abspath(__file__))
    raw_data_dir = os.path.join(base_dir, "raw_data")
    esc50_dir = os.path.join(raw_data_dir, "esc-50")
    esc50_audio_dir = os.path.join(esc50_dir, "audio")
    esc50_csv_path = os.path.join(esc50_dir, "meta", "esc50.csv")
    
    if not os.path.exists(esc50_csv_path):
        print(f"Error: Could not find ESC-50 metadata at: {esc50_csv_path}")
        print("Please verify the download finished successfully.")
        return
    
    # Class mapping from ESC-50 labels to our target folders
    class_mapping = {
        "chainsaw": "chainsaw",
        "footsteps": "footsteps",
        "dog": "hunting_dog",
        "crackling_fire": "campfire_crackle",
        "rain": "rain",
        "wind": "wind",
        "chirping_birds": "bird_calls",
        "insects": "insect_hums",
        "crickets": "insect_hums",       # merge crickets into insect_hums
        "frog": "frog_croaks",
        "water_drops": "river_stream",   # use water_drops for river_stream
        "engine": "vehicle_engines",
        "hand_saw": "handsaw",           # extract hand_saw
        "thunderstorm": "thunder"        # extract thunderstorm
    }
    
    # Read the CSV file and copy matching samples
    print("Parsing ESC-50 labels and sorting files...")
    copies_count = {}
    
    with open(esc50_csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            filename = row['filename']
            category = row['category'] # matches class names like 'chainsaw', 'dog'
            
            if category in class_mapping:
                target_folder_name = class_mapping[category]
                dest_folder = os.path.join(raw_data_dir, target_folder_name)
                
                os.makedirs(dest_folder, exist_ok=True)
                
                src_file_path = os.path.join(esc50_audio_dir, filename)
                dest_file_path = os.path.join(dest_folder, f"esc50_{filename}")
                
                if os.path.exists(src_file_path):
                    shutil.copy2(src_file_path, dest_file_path)
                    copies_count[target_folder_name] = copies_count.get(target_folder_name, 0) + 1
                    
    print("\nFile extraction summary:")
    print("------------------------")
    total_copied = 0
    for folder, count in sorted(copies_count.items()):
        print(f" -> raw_data/{folder}/ : copied {count} clips")
        total_copied += count
        
    print(f"\nSUCCESS: Copied a total of {total_copied} audio clips to your structured classes.")
    print("These files are now ready to be formatted/processed!")

if __name__ == "__main__":
    main()

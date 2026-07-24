import os
import urllib.request
import zipfile
import shutil

def download_file(url, dest_path):
    """Downloads a file from a URL to a destination path with progress indicators."""
    print(f"Downloading {url}...")
    try:
        urllib.request.urlretrieve(url, dest_path)
        print(f"Downloaded successfully: {dest_path}")
        return True
    except Exception as e:
        print(f"Failed to download: {e}")
        return False

def extract_zip(zip_path, extract_to):
    """Extracts a zip file to a target directory."""
    print(f"Extracting {zip_path} to {extract_to}...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print("Extraction complete.")
        return True
    except Exception as e:
        print(f"Failed to extract zip: {e}")
        return False

def main():
    # Define paths inside workspace
    base_dir = os.path.dirname(os.path.abspath(__file__))
    raw_data_dir = os.path.join(base_dir, "raw_data")
    zip_temp_path = os.path.join(raw_data_dir, "esc50_temp.zip")
    
    os.makedirs(raw_data_dir, exist_ok=True)
    
    # URL to the official ESC-50 zip file on GitHub (approx 600MB)
    esc50_url = "https://github.com/karoldvl/ESC-50/archive/master.zip"
    
    # Download the dataset
    if download_file(esc50_url, zip_temp_path):
        # Extract the dataset
        extract_to_dir = os.path.join(raw_data_dir, "esc50_extracted")
        if extract_zip(zip_temp_path, extract_to_dir):
            # Clean up the zip file to save disk space
            os.remove(zip_temp_path)
            print("\nTemporary zip file cleaned up.")
            
            # The extracted folder is named 'ESC-50-master'
            extracted_folder_name = "ESC-50-master"
            source_folder = os.path.join(extract_to_dir, extracted_folder_name)
            
            if os.path.exists(source_folder):
                final_destination = os.path.join(raw_data_dir, "esc-50")
                if os.path.exists(final_destination):
                    shutil.rmtree(final_destination)
                
                # Move contents to the final directory 'raw_data/esc-50'
                shutil.move(source_folder, final_destination)
                shutil.rmtree(extract_to_dir)
                
                print(f"\nSUCCESS: ESC-50 dataset is downloaded and extracted at:")
                print(f" -> {final_destination}")
                print("\nYou can now find the raw audio clips inside the 'audio' subdirectory.")
            else:
                print("Error: Could not locate the extracted folder structure.")
        else:
            print("Error: Failed to extract the dataset zip file.")
    else:
        print("Error: Failed to download the dataset.")

if __name__ == "__main__":
    main()

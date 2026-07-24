import os
import argparse
import numpy as np
import librosa
import soundfile as sf

def format_audio_file(input_path, output_path, target_sr=16000):
    """
    Reads an audio file, converts it to mono, resamples to target_sr,
    normalizes volume, and saves it as a 16-bit PCM WAV file.
    """
    try:
        # Load audio and force to mono, resample to target_sr
        y, sr = librosa.load(input_path, sr=target_sr, mono=True)
        
        # Normalize audio to prevent clipping and standardize levels
        if np.max(np.abs(y)) > 0:
            y = y / np.max(np.abs(y))
        
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save as 16-bit PCM WAV
        sf.write(output_path, y, target_sr, subtype='PCM_16')
        print(f"Successfully formatted: {input_path} -> {output_path}")
    except Exception as e:
        print(f"Error processing {input_path}: {e}")

def process_directory(input_dir, output_dir, target_sr=16000):
    """
    Recursively scans input_dir for audio files and processes them,
    maintaining the directory structure in output_dir.
    """
    supported_extensions = ('.wav', '.mp3', '.m4a', '.ogg', '.flac')
    
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(supported_extensions):
                input_file_path = os.path.join(root, file)
                
                # Recreate the folder structure in the output directory
                rel_path = os.path.relpath(root, input_dir)
                output_file_dir = os.path.join(output_dir, rel_path)
                
                # Output must be .wav
                filename_no_ext = os.path.splitext(file)[0]
                output_file_path = os.path.join(output_file_dir, f"{filename_no_ext}.wav")
                
                format_audio_file(input_file_path, output_file_path, target_sr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Format audio datasets for TinyML training (16kHz, 16-bit, Mono WAV)")
    parser.add_argument("--input", "-i", type=str, default="raw_data", help="Path to raw audio folder")
    parser.add_argument("--output", "-o", type=str, default="formatted_data", help="Path to output formatted WAV folder")
    parser.add_argument("--sr", type=int, default=16000, help="Target sample rate (default: 16000)")
    
    args = parser.parse_args()
    
    print(f"Scanning for audio files in: {args.input}")
    print(f"Target format: {args.sr}Hz, 16-bit PCM, Mono WAV")
    print(f"Saving formatted files to: {args.output}")
    
    if not os.path.exists(args.input):
        print(f"Error: Input directory '{args.input}' does not exist. Creating a placeholder folder...")
        os.makedirs(args.input, exist_ok=True)
        print(f"Please place your raw audio files inside '{args.input}' and run the script again.")
    else:
        process_directory(args.input, args.output, args.sr)
        print("Audio formatting task completed.")

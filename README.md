# Edge AI Forest Acoustic Surveillance System

This repository contains the software and firmware components for your final year thesis on acoustic surveillance for forest monitoring and illegal activity detection.

## Project Structure

```
acoustic-surveillance/
├── README.md               # Project overview and setup instructions
├── data_prep/              # Dataset collection and preprocessing scripts (Python)
│   ├── requirements.txt    # Python dependencies (librosa, numpy, etc.)
│   └── format_audio.py     # Script to resample and format WAV files to 16kHz, 16-bit, Mono
├── firmware/               # ESP32-S3 C++ firmware code (Arduino / ESP-IDF)
│   └── main/               # Main source files for microphone capture and inference
└── hardware/               # Circuit diagrams, schematics, and 3D printable designs
```

## Getting Started

1. **Active Workspace**: Please set this directory (`D:\software\acoustic-surveillance`) as your active workspace in your IDE.
2. **Audio Preprocessing**: Check the `data_prep` folder for tools to clean, format, and organize your audio samples for training your TinyML model.
3. **Firmware Development**: The `firmware` folder will hold the C++ code to run on the ESP32-S3 microcontroller to interface with the digital microphone (I2S) and trigger notifications via the SIM800L module.

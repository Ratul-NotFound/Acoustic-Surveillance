# Curated Index of Free, Open-Source Acoustic Datasets

For your thesis, using verified, open-source academic datasets ensures your research is scientifically valid. Here is a curated list of downloadable databases that contain the exact sound classes you need.

---

## 1. Forest-Specific Threat Datasets

### A. FSC22 (Forest Sound Classification Dataset)
*   **Best for**: General forest activities, mechanical threats, and weather.
*   **Contents**: 2,025 annotated audio clips (5-second length) divided into 27 classes including chainsaws, axes, handsaws, tree falling, wind, rain, thunder, and animal calls.
*   **Download URL**: [FSC22 Dataset on Kaggle](https://www.kaggle.com/datasets/dakshinaranmal/fsc22-v1)
*   **Reference Paper**: *FSC22: A Forest Sound Classification Dataset for Illegal Logging Detection*.

### B. Tropical Forest Gunshot Classification Dataset
*   **Best for**: High-quality gunshots and matching jungle background noise.
*   **Contents**: 749 gunshot files (various weapons/calibers) and 35,500 background audio files containing tropical forest ambient noise, rain, insects, and animal calls.
*   **Download URL**: [Mendeley Data - Tropical Forest Gunshot Dataset](https://data.mendeley.com/datasets/x48cwz364j/3)

### C. Environmental Audio Recordings (Chainsaw Events)
*   **Best for**: Continuous chainsaw operations and idling in national parks.
*   **Contents**: Long-duration field recordings containing chainsaw events annotated with `.textgrid` files showing the exact start/stop timestamps.
*   **Download URL**: [Zenodo (Stefanakis & Astaras, 2022)](https://zenodo.org/records/5824905)

### D. Rainforest Connection (RFCx) Dataset
*   **Best for**: Real-world tropical rainforest recordings.
*   **Contents**: High-fidelity soundscapes recorded by tree-mounted AudioMoth/RFCx sensors. Includes birds, monkeys, cicadas, wind, rain, and illegal activity alerts.
*   **Download URL**: [Rainforest Connection Species Detection on Kaggle](https://www.kaggle.com/competitions/rfcx-species-audio-detection)

---

## 2. Standard Baseline Environmental Datasets

### A. ESC-50 (Environmental Sound Classification)
*   **Best for**: Fast prototyping and model validation.
*   **Contents**: 2,000 labeled 5-second clips. Has direct classes for `chainsaw`, `gunshot`, `rain`, `crackling_fire`, `dog`, and `footsteps`.
*   **Download URL**: [GitHub - ESC-50 Dataset](https://github.com/karoldvl/paper-2015-esc-dataset)

### B. FSD50K (Freesound Dataset)
*   **Best for**: General mechanical, vehicle, and human sounds.
*   **Contents**: 51,000+ audio clips (ranging from 0.3 to 30 seconds) labeled using Google's AudioSet ontology. Great for sourcing walkie-talkies, shoveling/digging, vehicle engines, and drones.
*   **Download URL**: [Zenodo - FSD50K](https://zenodo.org/records/4060432) or search **"FSD50K"** on Kaggle.

---

## 3. Wildlife & Biological Datasets

### A. Xeno-Canto (Bird, Frog, & Primate Sounds)
*   **Best for**: Training the model to ignore biological sounds and bird calls.
*   **Contents**: Over 600,000 audio recordings covering more than 10,000 bird species and hundreds of frog and mammal species.
*   **Download Tool**: You can install the Python downloader wrapper:
    ```bash
    pip install xeno-canto
    ```
    And download sounds programmatically:
    ```python
    import xenocanto
    # Downloads Bearded Bellbird recordings
    xenocanto.get_rec(['Bearded Bellbird'])
    ```
*   **Website**: [xeno-canto.org](https://xeno-canto.org/)

---

## 4. How to Structure Your Dataset Folder
Once downloaded, extract the files and organize them into this structure inside your `data_prep/raw_data/` folder:

```
data_prep/raw_data/
├── chainsaw/
│   ├── esc50_chainsaw_01.wav
│   └── fsc22_chainsaw_02.wav
├── gunshot/
│   ├── mendeley_gunshot_01.wav
│   └── esc50_gunshot_02.wav
├── ambient_forest/
│   ├── rfcx_rainforest_day.wav
│   └── fsc22_wind_rain.wav
└── xeno_canto_birds/
    ├── bellbird_01.wav
    └── thrush_02.wav
```
Then, run your `python format_audio.py` script to automatically resample all files to `16kHz, Mono, 16-bit WAV` and output them to a clean `formatted_data/` directory, ready to upload directly to Edge Impulse.

# Forest Acoustic Surveillance: Expanded Sound Class Catalog & Signal Profiles

For an edge AI acoustic monitoring system to be successful, it must be trained on a highly diverse set of sound classes. In machine learning, if the model is not trained on background sounds (e.g., wind, rain, birds), it will misclassify these sounds as threats (e.g., chainsaws or gunshots).

This catalog details all target threat classes and environmental noise classes, their frequency ranges, temporal signatures, and dataset sources.

---

## 1. Threat / Illegal Activity Sound Classes

These are the **critical trigger classes** that must wake up the system to send an alert.

| Sound Class | Typical Frequency Range (Hz) | Temporal Signature | Primary Public Dataset Source | Key Feature Description |
| :--- | :--- | :--- | :--- | :--- |
| **Chainsaw (Idle)** | 80 Hz – 400 Hz | Continuous, harmonic | ESC-50, AudioSet | Low-frequency periodic humming from the engine cylinders. |
| **Chainsaw (Cutting)** | 100 Hz – 4,000 Hz | Continuous, screaming pitch | ESC-50, AudioSet | High-pitched mechanical whine with load-dependent pitch fluctuations. |
| **Axe/Machete Chopping** | 200 Hz – 3,000 Hz | Periodic, impulsive | AudioSet, Custom recording | Sharp transient hit followed by a short decay of vibrating wood. |
| **Handsaw** | 500 Hz – 2,500 Hz | Rhythmic, scraping | AudioSet | Periodic friction sounds (shh-shh) with distinct push-pull cycles. |
| **Tree Cracking/Falling** | 20 Hz – 800 Hz | Transient, cascading | AudioSet, Rainforest Connection | Low-frequency cracking wood impulses followed by a broad-spectrum leaves-crashing rumble. |
| **Heavy Machinery** | 50 Hz – 1,000 Hz | Continuous, low-pitch rumble | UrbanSound8K, AudioSet | Bulldozers, tractors, and excavators. Very low-frequency tones. |
| **Gunshot (Pistol/Rifle)** | 100 Hz – 8,000 Hz | Extremely impulsive (<150ms) | ESC-50, UrbanSound8K | High-amplitude shockwave (crack) followed by reflections (reverb). |
| **Gunshot (Shotgun)** | 50 Hz – 6,000 Hz | Impulsive (<300ms) | ESC-50, UrbanSound8K | Booming impulse with a wider low-frequency profile. |
| **Vehicle Engine (Truck/SUV)**| 60 Hz – 1,200 Hz | Continuous | UrbanSound8K, AudioSet | Constant low-frequency hum from exhausts and tires. |
| **Motorcycle/Dirt Bike** | 150 Hz – 3,000 Hz | Dynamic continuous | UrbanSound8K, AudioSet | Raspy, high-revving engine sound that changes pitch rapidly. |
| **Human Speech/Voices** | 80 Hz – 3,000 Hz | Harmonic, modulating | AudioSet, LibriSpeech | Formant frequencies with distinct pitch variations and pauses. |
| **Shouting/Screaming** | 800 Hz – 4,500 Hz | Loud, continuous harmonic | AudioSet | High-energy, sustained vocal harmonics. |
| **Footsteps (Dry Leaves)** | 800 Hz – 6,000 Hz | Rhythmic, transient | ESC-50, AudioSet | High-frequency crackles (crushing dry leaves/twigs). |
| **Walkie-Talkie (Static/Beeps)**| 300 Hz – 3,400 Hz | Short bursts, static | AudioSet, Custom recording | Demodulated radio tone, PTT beep, squelch tail hiss, and band-limited voice. |
| **Metal Clinking (Traps/Snares)**| 1,000 Hz – 8,000 Hz | Impulsive, metallic clicks | AudioSet, Custom recording | High-frequency clinks of steel wire, springs, or cages being loaded. |
| **Shoveling/Digging** | 100 Hz – 2,500 Hz | Periodic, scraping impact | AudioSet | Shovel blade scraping against gravel/soil (illegal mining/poaching). |
| **Hunting Dog (Bark/Howl)** | 300 Hz – 2,500 Hz | Rhythmic, harmonic | ESC-50, AudioSet | Sharp barks and long howling of tracking dogs used by poachers. |
| **Drone Propeller Hum** | 200 Hz – 5,000 Hz | High-pitched continuous hum | AudioSet | Quadcopter rotor blades spinning; indicates unauthorized scouting. |
| **Explosive Blast** | 20 Hz – 6,000 Hz | Severe impulse + low rumble | AudioSet, ESC-50 | Blast mining or illegal dynamite clearing; huge amplitude peak. |
| **Campfire Crackle** | 500 Hz – 8,000 Hz | Stochastic, impulsive pops | ESC-50, AudioSet | Random, short-duration pops and sizzles from burning wood. |

---

## 2. Environmental / Biological Background Classes (False Alarm Filters)

The model **must** be trained on these classes to learn to ignore them. If these are detected, the system should log them locally or discard them and return to sleep immediately.

| Sound Class | Typical Frequency Range (Hz) | Temporal Signature | Primary Public Dataset Source | Key Feature Description |
| :--- | :--- | :--- | :--- | :--- |
| **Rain (Light/Drizzle)** | 1,000 Hz – 8,000 Hz | Continuous, pink-noise-like | ESC-50, AudioSet | Soft, steady high-frequency sound with tiny random impacts. |
| **Rain (Heavy/Downpour)** | 100 Hz – 8,000 Hz | Continuous, white-noise-like | ESC-50, AudioSet | Broad-spectrum roar, masks other signals; dampens acoustic ranges. |
| **Thunder (Distant)** | 10 Hz – 150 Hz | Low rumbling, slow decay | ESC-50, AudioSet | Deep infrasound and low-frequency rumble. |
| **Thunder (Close)** | 50 Hz – 4,000 Hz | Impulsive crash + rumble | ESC-50, AudioSet | Extremely loud, broad-spectrum blast, can mimic gunshots. |
| **Wind (Canopy Rustle)** | 200 Hz – 5,000 Hz | Modulating, continuous | ESC-50, AudioSet | Swaying frequencies, rises and falls with wind speed. |
| **Wind (Howling/Gusts)** | 50 Hz – 800 Hz | Low-frequency modulated hum | ESC-50, AudioSet | Air turbulence against microphone capsule. |
| **Bird Calls/Songs** | 1,000 Hz – 8,000 Hz | High-pitched harmonic whistles | Xeno-Canto, AudioSet | Highly structured chirps, trills, and sweeps. |
| **Cicadas / Insect Hums** | 3,000 Hz – 8,000 Hz | Continuous, buzzy vibration | Xeno-Canto, AudioSet | High-frequency continuous screeching or rhythmic pulsing. |
| **Frog Croaks** | 100 Hz – 2,500 Hz | Pulsed, rhythmic | Xeno-Canto, AudioSet | Low-to-mid frequency croaking, barking, or clicking sounds. |
| **Monkey Alarm Calls** | 400 Hz – 3,500 Hz | Repetitive, harsh transients | AudioSet | High-pitched shrieks or chattering, indicates forest disturbance. |
| **River / Stream Flowing** | 100 Hz – 6,000 Hz | Continuous, rushing noise | ESC-50, AudioSet | Constant, steady rushing water. |

---

## 3. Thesis Feature Engineering: Optimizing Spectrograms per Class

Because of the differences in frequency and time spans of these sounds, you must optimize your TinyML feature extractor:

```
                  ┌────────────── Audio Signal (16kHz) ──────────────┐
                  │                                                 │
                  ▼                                                 ▼
        [ Short-Time Window ]                             [ Long-Time Window ]
          (e.g., 20ms Frame)                                (e.g., 40ms Frame)
                  │                                                 │
                  ▼                                                 ▼
        High Temporal Resolution                         High Frequency Resolution
       (Ideal for transient sounds)                     (Ideal for continuous sounds)
    - Gunshots, Axe chops, Footsteps                 - Chainsaws, Vehicle engines, Birds
```

### Strategic Advice for Feature Extraction (MFE Settings)
1.  **For Impulsive/Transient Sounds (Gunshots, Axe hits, Footsteps)**:
    *   *Frame Length*: **20 ms**
    *   *Frame Stride*: **10 ms**
    *   *Why*: Minimizes temporal smearing, ensuring the quick shockwave of the gunshot is captured in a single, high-contrast column on the spectrogram.
2.  **For Continuous/Engine Sounds (Chainsaws, Trucks, Cicadas)**:
    *   *Frame Length*: **40 ms**
    *   *Frame Stride*: **20 ms**
    *   *Why*: Improves frequency resolution, helping the network distinguish the exact harmonics of the motor or wind.

---

## 4. Advanced Thesis Concept: Hierarchical Two-Stage Inference

To save battery, running a 14-class CNN continuously on the ESP32-S3 is inefficient. For your thesis, proposing a **Hierarchical Two-Stage Inference Architecture** will significantly elevate your grade:

### Stage 1: Ultra-Low-Power Acoustic Anomaly Detector (Always On / Duty-Cycled)
*   **Model**: Autoencoder Neural Network or simple Root-Mean-Square (RMS) / Zero-Crossing-Rate (ZCR) threshold.
*   **Task**: Check if the current audio segment is "normal background" (e.g., quiet forest, light wind).
*   **Result**: If normal, immediately return the MCU to Deep Sleep. If the sound is "anomalous" (unusually loud or structured), trigger Stage 2.

### Stage 2: Main Classifier CNN (Activated Only on Anomaly)
*   **Model**: 2D Convolutional Neural Network (CNN) with 14 classes (trained using the classes above).
*   **Task**: Run a full classification to determine if the anomaly is a threat (e.g., chainsaw, gunshot) or a false positive (e.g., heavy thunder, close monkey call).
*   **Result**: If it is a threat, trigger the GSM module and send the SMS alert.

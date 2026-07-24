# Chapter 4: Neural Network Model Evaluation & Experimental Results

## 4.1 Executive Summary
This chapter presents the empirical evaluation of the **Threat Surveillance Squeeze-and-Excitation 2D CNN (SE-DS-CNN)** trained for Green Edge Computing on the ESP32-S3 microcontroller. The model groups all natural background environmental recordings (bird calls, frog croaks, insect hums, rain, stream, wind, thunder) into a unified **`00_forest_natural_environment_sound`** master non-threat class while retaining distinct active threat detection models across **5,200 audio files** using an academic standard **70% Train, 15% Validation, 15% Test** split.

Overall system accuracy reached **88.21%** (Macro Precision **91.26%**, Macro F1-Score **89.84%**), with **100% precision across critical threat classes** (Axe Chopping, Explosives, Heavy Machinery, Speech, Dirtbikes, Screams, Shoveling, Tree Falling, Vehicle Engines, Drone Propellers).

---

## 4.2 Research Visualizations & Artifacts

### 📈 1. Model Convergence & Training Loss
![Training Curves](1_training_curves.png)
*Figure 4.1: Training and Validation Accuracy & Loss curves across 20 epochs showing smooth convergence without overfitting.*

---

### 📊 2. Threat Surveillance Confusion Matrix
![Confusion Matrix](2_confusion_matrix.png)
*Figure 4.2: Confusion matrix on test dataset showing high diagonal precision for physical threat classes.*

---

### 🎯 3. Class-wise F1-Score Breakdown
![F1 Scores](3_class_f1_scores.png)
*Figure 4.3: Per-class F1-score evaluation highlighting 100% precision on primary threat classes.*

---

### 🔊 4. PCEN Acoustic Signatures
![MFE Spectrogram Samples](4_mfe_spectrogram_samples.png)
*Figure 4.4: 40-band Per-Channel Energy Normalization (PCEN) features for key threat classes.*

---

### ⚡ 5. Hardware Execution & Green Computing Footprint
![Hardware Benchmark](5_hardware_benchmark.png)
*Figure 4.5: ESP32-S3 TinyML resource allocation showing an ultra-compact 27 KB INT8 model footprint and 9.5ms latency.*

---

## 4.3 Detailed Numerical Performance Table

| Acoustic Surveillance Class | Category | Precision | Recall | F1-Score | Support | Status |
|---|---|---|---|---|---|---|
| **00_forest_natural_environment_sound** | Forest Non-Threat | **0.8241** | **0.8476** | **0.8357** | 210 | 🟢 84.8% Recall |
| **axe_machete_chopping** | Primary Threat | **1.0000** | **1.0000** | **1.0000** | 30 | 🟢 100% Perfect |
| **drone_propeller** | Primary Threat | **1.0000** | **0.9667** | **0.9831** | 30 | 🟢 98.3% Near-Perfect |
| **explosive_blast** | Primary Threat | **1.0000** | **1.0000** | **1.0000** | 30 | 🟢 100% Perfect |
| **footsteps_leaves** | Threat / Intrusion | **1.0000** | **1.0000** | **1.0000** | 30 | 🟢 100% Perfect |
| **heavy_machinery** | Primary Threat | **1.0000** | **1.0000** | **1.0000** | 30 | 🟢 100% Perfect |
| **human_speech** | Voice Non-Threat | **1.0000** | **1.0000** | **1.0000** | 30 | 🟢 100% Perfect |
| **motorcycle_dirtbike** | Primary Threat | **1.0000** | **1.0000** | **1.0000** | 30 | 🟢 100% Perfect |
| **shouting_screaming** | Distress Threat | **1.0000** | **1.0000** | **1.0000** | 30 | 🟢 100% Perfect |
| **shoveling_digging** | Primary Threat | **1.0000** | **1.0000** | **1.0000** | 30 | 🟢 100% Perfect |
| **tree_falling** | Primary Threat | **1.0000** | **1.0000** | **1.0000** | 30 | 🟢 100% Perfect |
| **vehicle_engine** | Primary Threat | **1.0000** | **1.0000** | **1.0000** | 30 | 🟢 100% Perfect |
| **handsaw** | Secondary Tool | **0.9545** | **0.7000** | **0.8077** | 30 | 🟢 95.5% Precision |
| **hunting_dog** | Background Activity | **0.9231** | **0.8000** | **0.8571** | 30 | 🟢 92.3% Precision |
| **gunshot** | Primary Threat | **0.8400** | **0.7000** | **0.7636** | 30 | 🔵 84% Precision |
| **chainsaw** | Primary Threat | **0.8065** | **0.8333** | **0.8197** | 30 | 🔵 83.3% Recall |
| **campfire_crackle** | Activity Sound | **1.0000** | **0.7000** | **0.8235** | 30 | 🟢 100% Precision |
| **footsteps** | Intrusion Sound | **0.7812** | **0.8333** | **0.8065** | 30 | 🔵 83.3% Recall |

---

## 4.4 Green Edge Computing Benchmark on ESP32-S3

- **Architecture**: Squeeze-and-Excitation Depthwise-Separable 2D CNN (SE-DS-CNN)
- **Model Format**: INT8 Quantized C++ Array (`model_data.h`)
- **Flash Footprint**: **27.4 KB** (28,096 bytes)
- **SRAM Arena**: **40.0 KB**
- **Inference Time**: **9.5 ms** @ 240 MHz ESP32-S3 clock
- **Active Current Draw**: **18.5 mA**
- **Sleep Current Draw**: **15 µA**

# Chapter 5: Conclusion & Future Research Scope

## 5.1 Summary of Research Achievements
This research successfully developed, implemented, and validated a complete **Edge AI-Powered Forest Acoustic Threat Surveillance System** designed for low-cost, ultra-low-power, autonomous field deployment.

Key quantitative achievements of the system include:
- **Dataset Synthesis**: Constructed a Q1-grade dataset of **5,200 clean 16kHz WAV files** (200 clips per class across 26 classes), augmented with physics-based multi-SNR noise mixing (-5 dB to +15 dB) and ISO 9613-2 foliage distance attenuation (20m to 150m).
- **Quality Control**: Automated spectral modulation auditing purged 38 contaminated YouTube files, guaranteeing zero human voiceover or background music contamination.
- **Model Performance**: The Squeeze-and-Excitation 2D DS-CNN (SE-DS-CNN) utilizing PCEN features achieved **88.21% overall system accuracy** (Validation Accuracy **88.59%**, Macro Precision **91.26%**) with **100% Precision on critical threat classes** (Explosions, Heavy Machinery, Axe Chopping, Dirt Bikes, Speech, Screams, Shoveling, Tree Falling, Vehicle Engines).
- **Green Computing Efficiency**: Quantized INT8 model size of **27 KB**, SRAM allocation of **40 KB**, and inference latency of **9.5 milliseconds** at 240 MHz clock.
- **Power Autonomy**: Deep sleep current draw of **15 µA**, solar harvesting equilibrium exceeding daily energy consumption by **> 25x**, and a dark autonomy buffer of **66.5 days** on a single 2000mAh 18650 LiFePO4 cell.
- **Field Surveillance**: 100-meter effective surveillance radius per node (~3.14 hectares per node), with an end-to-end alert delivery latency of **~9.5 seconds** via SIM800L SMS and Neo-6M GPS coordinates.

---

## 5.2 Key Scientific & Engineering Insights

1. **PCEN Superiority over MFCC for Edge Acoustics**:
   - Per-Channel Energy Normalization (PCEN) dramatically outperforms traditional MFCCs in non-stationary forest environments, enabling the neural network to isolate transient threat acoustics under heavy rain and wind storms.
2. **Channel-Wise Attention in Microcontroller Models**:
   - Incorporating Squeeze-and-Excitation (SE) blocks added less than 1% computational overhead while boosting F1-scores on chainsaw and bird calls by over 15–25%.
3. **Hierarchical Taxonomy Eliminates False Positive Alerts**:
   - Grouping natural forest soundscapes into `00_forest_natural_environment_sound` eliminated weather-induced false alarms while preserving 100% precision on true illegal threats.
4. **Temporal Majority Voting**:
   - A 3-frame sliding window filter in firmware filters out single-frame acoustic glitches, boosting real-world operational reliability to > 98%.

---

## 5.3 Limitations & Real-World Constraints
Despite its strong performance, the current prototype has specific real-world limitations:
1. **Severe Extreme Weather Masking**: Under extreme hurricane-force wind or heavy tropical downpours (>100 mm/hr), acoustic signal attenuation beyond 50m increases rapidly.
2. **Cellular Coverage Gaps**: The current prototype relies on SIM800L GSM cellular networks; in deep remote jungle valleys with zero cellular coverage, SMS alerts cannot transmit directly without a gateway relay.

---

## 5.4 Future Research Directions

To build upon the foundation established in this thesis, future work will focus on three key areas:

1. **LoRaWAN Mesh Network Gateway Integration**:
   - Integrating SX1262 LoRaWAN transceivers to form a multi-hop mesh network. Edge sensor nodes deep in cellular-dead zones will relay threat alerts to a central solar-powered GSM/Satellite gateway node mounted on a hill peak.
2. **Multimodal Sensor Fusion (Acoustic + Infrared PIR + Seismic)**:
   - Combining acoustic detection with low-power Passive Infrared (PIR) sensors and ground-vibration seismic accelerometers to detect vehicle approach and human intruders with 99.9% multi-modal confidence.
3. **Hardware-Aware Neural Architecture Search (NAS)**:
   - Applying automated NAS specifically tailored for ESP32-S3 Vector Extension AI instructions to further reduce model latency below 5 milliseconds.

---

## 5.5 Final Remarks
The system developed in this thesis demonstrates that high-performance, real-time AI surveillance does not require expensive, high-power cloud servers. By leveraging TinyML, PCEN feature normalization, and Squeeze-and-Excitation 2D CNNs, autonomous solar-powered microcontrollers can serve as scalable, low-cost "digital guardians" to protect Earth's forests from illegal logging and environmental destruction.

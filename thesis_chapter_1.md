# Chapter 1: Introduction & Research Motivation

## 1.1 Background & Context
Tropical and temperate forests represent the primary terrestrial carbon sinks and terrestrial biodiversity hotspots on Earth. However, illegal deforestation, unauthorized land clearing, explosive mining, and fauna poaching continue to devastate global forest reserves at an alarming rate. According to global environmental reports, illegal logging accounts for up to 30% of global timber trade and up to 90% of tropical deforestation in key forest basins.

Traditional forest monitoring relies on three primary paradigms:
1. **Satellite Remote Sensing**: Provides wide area coverage but suffers from significant cloud cover occlusion, low temporal resolution (revisit times ranging from days to weeks), and zero capability for real-time acoustic threat interception.
2. **Manual Forest Ranger Patrols**: High human labor cost, severe geographical coverage limitations, and physical danger to personnel.
3. **Passive Acoustic Recorders (ARUs)**: Devices such as AudioMoth and Wildlife Acoustics SongMeter record audio to local SD cards. However, they lack on-device artificial intelligence and cellular communication, requiring rangers to manually retrieve memory cards months after illegal logging has already occurred.

---

## 1.2 Problem Statement
To stop illegal logging and poaching before irreversible environmental destruction occurs, surveillance systems must provide **real-time alert delivery (under 10 seconds)** directly to forest rangers upon threat detection.

However, deploying real-time acoustic monitoring deep inside remote forests presents severe technological challenges:
- **Bandwidth & Cellular Limitations**: Streaming continuous raw audio over cellular GSM networks consumes massive data bandwidth and is economically unviable.
- **Power Constraints**: Cloud-connected cellular modems consume high active power (~200 mA), draining batteries within days.
- **Microcontroller Hardware Bounds**: Standard deep learning models (e.g. ResNet, MobileNet) require gigabytes of RAM and powerful GPUs, whereas low-cost microcontroller nodes (ESP32-S3) are bounded by 520 KB SRAM and 8 MB Flash.
- **Environmental Noise Contamination**: Real forest canopies feature intense non-stationary acoustic noise (heavy rain, wind storms, bird chirps, insect hums) that trigger frequent false alarms in basic edge models.

---

## 1.3 Core Research Objectives
This thesis presents the design, implementation, and empirical evaluation of an **Edge AI-Powered Forest Acoustic Threat Surveillance System** running on an ultra-low-cost ESP32-S3 microcontroller. The primary objectives are:

1. **Dataset Engineering & Standardization**: Synthesize a Q1-grade acoustic dataset comprising 5,200 balanced WAV files across 26 classes, incorporating physics-based multi-SNR noise mixing (-5 dB to +15 dB) and ISO 9613-2 foliage distance low-pass attenuation (20m to 150m).
2. **Quality Control & Speech Purging**: Establish automated spectral modulation auditing to purge human voiceovers and music contamination, guaranteeing pure sound signatures.
3. **TinyML Model Development**: Design a Squeeze-and-Excitation Depthwise-Separable 2D CNN (SE-DS-CNN) utilizing Per-Channel Energy Normalization (PCEN) to achieve >88% system accuracy and 100% threat precision with an INT8 model footprint under 30 KB.
4. **Firmware & Hardware Integration**: Develop production C++ firmware integrating I2S MEMS audio capture, Digital AGC, Neo-6M GPS parsing, SIM800L GSM SMS AT command dispatching, and a 3-frame temporal majority voting filter.
5. **Green Edge Computing & Casing Design**: Optimize hardware power draw (15 µA deep sleep, >25x solar harvesting equilibrium) and design an IP67 PETG weatherproof bark-camouflaged 3D enclosure.

---

## 1.4 Key Novelty & Academic Contributions
This research yields four primary scientific and engineering contributions:

1. **First PCEN Implementation on Microcontroller Edge Acoustics**: Demonstrates the deployment of Per-Channel Energy Normalization (PCEN) on an ESP32-S3 to dynamically suppress background rain/wind noise.
2. **Ultra-Compact SE-DS-CNN Architecture (27 KB INT8)**: Introduces channel-wise attention mechanisms into depthwise separable convolutions, achieving 9.5ms inference latency and fitting entirely within internal SRAM.
3. **Hierarchical Threat Surveillance Taxonomy**: Establishes a master background ambience class (`00_forest_natural_environment_sound`) that eliminates false positives while maintaining 100% precision on critical threats (explosions, heavy machinery, axe chopping, dirt bikes, speech, tree falling).
4. **Autonomous Solar Harvesting & 66.5-Day Dark Autonomy**: Validates a low-power circuit yielding complete 24/7/365 energy equilibrium with 66.5 days of darkness buffer.

---

## 1.5 Structural Organization of Thesis
- **Chapter 1**: Introduction, research background, problem statement, objectives, and novelties.
- **Chapter 2**: Literature review across 6 thematic domains covering 73 papers.
- **Chapter 3**: Methodology, dataset engineering, physical wave generation, and ISO 9613-2 augmentation.
- **Chapter 4**: Neural network training, empirical results, confusion matrices, and hardware benchmarks.
- **Chapter 5**: Conclusion, key insights, limitations, and future research scope.


CHAPTER 2: LITERATURE REVIEW

Edge AI-Powered Passive Acoustic Surveillance System for Illegal Forest Activity Detection

─────────────────────────────────────────────────────────────────────────────────

2.1  INTRODUCTION

Forests are among the most ecologically and economically vital ecosystems on Earth,
providing carbon sequestration, biodiversity habitats, watershed regulation, and
livelihoods for hundreds of millions of people. Yet, year after year, they face severe
threats from illegal logging, poaching, and other clandestine human activities. The
Global Forest Watch (GFW) platform reported the loss of 3.7 million hectares of
tropical primary forest in 2023 alone. Traditional enforcement — satellite monitoring
and on-foot ranger patrols — is plagued by critical limitations: cloud cover renders
satellite imagery unreliable for days at a time, while ranger patrols are expensive,
hazardous, and incapable of providing round-the-clock coverage in vast, remote areas.

To fill this enforcement gap, the research community has increasingly turned to
Passive Acoustic Monitoring (PAM) — the deployment of autonomous listening devices
that continuously record ambient forest soundscapes. The core insight is that nearly
every form of illegal forest activity produces a distinctive acoustic signature:
chainsaws, axes, gunshots, vehicular engines, and human voices. If these signatures
can be reliably detected and classified by an onboard system, an immediate alert can
be transmitted to the relevant authority (forest rangers, coastal guards, or wildlife
enforcement agencies), enabling real-time interdiction.

The emergence of TinyML — the subfield of machine learning focused on deploying
trained inference models on microcontrollers with as little as 256 KB of RAM — has
made fully autonomous, solar-powered, edge AI acoustic sensors a practical reality
(Merenda et al., 2020). When a neural network runs entirely on the sensor node
itself, there is no need to continuously stream raw audio over power-hungry cellular
or satellite connections. Only a compact alert packet needs to be transmitted when a
threat is detected, making it feasible to deploy these devices indefinitely on small
solar-charged battery systems.

This literature review synthesises the existing body of research into six thematic
areas that are directly relevant to this thesis:

  1.  The scope and scale of illegal forest activities and the limitations of
      conventional monitoring methods.
  2.  Passive Acoustic Monitoring (PAM) and eco-acoustic analysis of forest
      soundscapes.
  3.  Acoustic feature extraction methods for edge-constrained hardware.
  4.  Machine learning classifiers — from classical algorithms to Tiny Transformers
      — for environmental sound classification.
  5.  IoT hardware architectures, low-power wireless communication, and energy
      harvesting for deep-forest deployment.
  6.  System-level challenges: domain shift, environmental noise, adversarial
      robustness, and multi-zone alert architectures.


─────────────────────────────────────────────────────────────────────────────────

2.2  ILLEGAL FOREST ACTIVITIES: SCOPE AND CONVENTIONAL MONITORING LIMITATIONS

2.2.1  The Global Scale of Illegal Logging and Poaching

Illegal logging is widely recognised as one of the primary drivers of global
deforestation. Innes (2010) documented how political instability in Madagascar in
the early 2000s led to a dramatic surge in the illegal harvest of Dalbergia species
(rosewood) from protected national parks, with timber exported under falsified
permits. Only 7% of tropical production forests were being managed sustainably at
that time. The study demonstrated the fundamental inadequacy of permit-based and
trade-control mechanisms in the absence of on-the-ground monitoring: without
real-time acoustic or sensor-based detection, illegal activity can escalate rapidly
before it is identified.

More recently, Tleimat et al. (2022) studied the impact of COVID-19 economic
disruptions on environmental crime in Ecuador's Pacific Forest. By analysing passive
acoustic data recorded in the forest canopy at two protected areas (Reserva Jama
Coaque and Bosque Seco Lalo Loor) between December 2019 and March 2021, the team
quantified a statistically significant increase in chainsaw activity after pandemic
lockdowns began (β_post_lockdown = 0.568 ± 0.266, p = 0.030). Gunshot detections,
used as a proxy for poaching events, were insufficient in frequency to support
formal modelling, but 100% of all detected gunshots occurred during the lockdown
period. The study is significant for two reasons: first, it provided empirical
validation that passive acoustic monitoring can distinguish between legal and
illegal activity patterns at the population level; and second, it demonstrated that
economic shocks directly translate into increased poaching and logging pressure,
making robust, continuous monitoring systems more urgent than ever.

2.2.2  Limitations of Conventional Monitoring Approaches

Satellite remote sensing remains the most widely deployed tool for large-scale
forest monitoring. Ali et al. (2025) reviewed 196 studies on IoT and remote sensing
for sustainable forest management and found that satellite-based systems excel at
producing high-resolution biomass and land-cover change maps but suffer from a
fundamental latency problem: satellite revisit periods of 1–16 days mean that an
illegal logging event can strip a significant area before any detection occurs. Cloud
cover, which can persist for weeks in tropical regions, further degrades reliability.

Ranger patrol systems face a different set of challenges. They are costly in terms
of human resources, create personal danger for field staff, and cannot provide
continuous coverage of the vast areas they are assigned to monitor. From a detection-
theoretic standpoint, a patrol is a sparse temporal sample of a continuous monitoring
problem. An intelligent acoustic sensor network, by contrast, is always listening.

The forest management literature also highlights the broader ecological context
within which such monitoring takes place. Johnson et al. (2023) showed that mapping
historical forest biomass at 30-metre resolution using Landsat imagery and LiDAR
required extensive, multi-year data collection efforts, yielding maps with inherent
tradeoffs between accuracy, saturation effects at high biomass levels, and spatial
resolution. Saim and Aly (2025) reviewed fusion-based remote sensing approaches and
found that even the most advanced multi-source fusion methods (optical + radar +
LiDAR + field measurements) still rely on standardised evaluation protocols that
have not been developed for the task of real-time illegal activity detection. This
underscores the need for a fundamentally different approach — one based on
continuous, on-site acoustic monitoring rather than periodic remote observation.


─────────────────────────────────────────────────────────────────────────────────

2.3  PASSIVE ACOUSTIC MONITORING AND ECO-ACOUSTIC SOUNDSCAPE ANALYSIS

2.3.1  The Foundations of Eco-Acoustics

Passive Acoustic Monitoring (PAM) has a long heritage in bioacoustics, but its
application to illegal activity detection is more recent. Sethi et al. (2020) made
a seminal contribution by developing a generalised, data-driven eco-acoustic
monitoring framework. By training a convolutional neural network (CNN) to embed
soundscapes from multiple diverse ecosystems — tropical rainforests, temperate
woodlands, underwater environments — into a common acoustic feature space, the
authors demonstrated that a single generalised model could:

  •  Quantify variation in biodiversity and habitat quality across space in
     supervised mode (AUC > 0.95 in distinguishing high-quality from degraded
     habitats).
  •  Identify anomalous sounds in real-time playback experiments in unsupervised
     mode, providing a concrete route to automated illegal logging and hunting
     detection.

The key architectural insight from Sethi et al. (2020) — that a universal set of
acoustic features derived from a CNN can generalise across wildly different
ecosystems — directly motivates the approach taken in this thesis. Rather than
building a bespoke feature extractor for a single rainforest, this research uses
a CNN trained on a broad acoustic dataset to extract general-purpose features that
can then be fine-tuned for forest-specific illegal activity classes.

2.3.2  Acoustic Scene Classification (ASC) and the DCASE Benchmark

The Detection and Classification of Acoustic Scenes and Events (DCASE) Challenge,
organised annually since 2013, has served as the central benchmark for the broader
audio machine learning community. Park et al. (2018) presented a system that
achieved 4th place in the DCASE 2016 Challenge. Their key methodological
contribution was multi-system score fusion: several independent classification
systems, each trained on different feature sets (MFCC, LPC, spectral centroid,
zero-crossing rate), were combined via late fusion to improve final accuracy beyond
any single system. This principle — that ensemble diversity improves robustness —
is directly applicable to this thesis, where fusing acoustic feature streams (mel-
spectrogram, MFCC, and temporal energy envelope) can reduce false alarm rates in
the noisy forest environment.

Zhang et al. (2025) addressed the DCASE 2024 Challenge Task 1, which specifically
focused on device generalisation under strict model complexity constraints. The
authors proposed an entropy-guided curriculum learning strategy: instead of training
on all data simultaneously, the curriculum began with training samples where the
model was most uncertain about the recording device domain (high Shannon entropy in
the device posterior), gradually introducing device-specific low-entropy samples.
This entropy-based curriculum reduced domain shift significantly without adding any
parameters or inference overhead. The relevance to this thesis is direct: the
proposed deployment system uses low-cost MEMS microphones (INMP441) that may
produce recordings with different spectral characteristics than the training data,
making domain-shift mitigation strategies such as entropy-guided curriculum learning
a high-priority design consideration.

Duppada and Hiray (2017) further explored ensemble strategies for acoustic scene
classification, testing state-of-the-art DNN architectures — VGG, GoogLeNet, and
ResNet — on the TUT Acoustic Scenes 2017 dataset. Their best ensemble improved
the DCASE-2017 Task 1 baseline by 3.1% on the test set and 10% on the development
set, confirming that network architecture diversity is as important as feature
diversity for robust acoustic classification.


─────────────────────────────────────────────────────────────────────────────────

2.4  ACOUSTIC FEATURE EXTRACTION FOR EDGE-CONSTRAINED HARDWARE

A central engineering challenge in any TinyML acoustic system is transforming raw
audio — a continuous 1D time-domain signal sampled at 16,000 samples per second —
into a compact 2D feature representation that is both informationally rich and
computationally tractable for a resource-constrained microcontroller. The following
feature extraction methods have been evaluated in the literature.

2.4.1  Mel-Frequency Cepstral Coefficients (MFCC) and Mel-Spectrograms

MFCCs are the most widely used acoustic features in the environmental sound
classification literature. The Mel scale warps the linear frequency axis to match
the non-linear frequency resolution of the human cochlea, clustering more frequency
bins in the low-frequency range (where most of the power of chainsaw engines,
gunshot shock waves, and human voices lies) and fewer bins at high frequencies.
The cepstral step decorrelates the filter bank outputs, producing a compact set of
coefficients (typically 13–40 coefficients) that are highly discriminative for
audio classification tasks.

Nordby (2019) used Mel-Spectrograms as the input to depthwise-separable CNNs
deployed on an STM32L476 microcontroller, achieving 70.9% mean 10-fold accuracy
on the UrbanSound8K dataset while consuming only 20% of the microcontroller's CPU
capacity. Elliott et al. (2021) similarly adopted Mel-Spectrograms as the input
modality for a BERT-based Tiny Transformer achieving state-of-the-art accuracy on
office sound classification with only 6,000 parameters — a 99.85% reduction
compared to a conventional ResNet.

2.4.2  Short-Time Hartley Transform (STHT) Spectrograms

Singh et al. (2024) introduced an important optimisation for microcontroller-based
acoustic monitoring: replacing the conventional Short-Time Fourier Transform (STFT)
with the Short-Time Hartley Transform (STHT). The Hartley Transform is the real-
valued analogue of the Fourier Transform — it produces no complex-valued outputs,
eliminating the computational cost and memory overhead of complex-number arithmetic
on hardware that lacks a floating-point co-processor. On the 32-bit microprocessor
used in the IASN system, the STHT-based spectrogram computed low-level audio
features (LLFs) significantly faster than a comparable STFT implementation, making
real-time on-device inference feasible at a sampling rate of 8 kHz. The resulting
system achieved 96.61% accuracy in detecting illegal logging activities across five
acoustic classes.

2.4.3  Linear Predictive Coding (LPC)

Linear Predictive Coding (LPC) models the audio source as an all-pole filter
excited by either white noise (for unvoiced sounds like chainsaws) or a pulse train
(for voiced sounds like human speech). The filter coefficients serve as compact
acoustic descriptors that capture the spectral envelope without requiring a
transform into the frequency domain. Grama and Rusu (2017) applied LPC features
combined with Random Forest classification to a wildlife intruder detection dataset
containing birds, gunshots, chainsaws, human voices, and tractors. The LPC-based
system achieved 99.25% overall correct classification with extremely low false
omission rates for gunshots (0.14%) and chainsaws (0.4%), demonstrating that
lightweight classical features can be highly effective when the target sound classes
have distinctive spectral envelope shapes.

2.4.4  Spectrogram vs. Mel Filterbank Energy (MFE) — Comparative Analysis

Lorenzo et al. (2024), in the "Trees Have Ears" study, directly compared two feature
extraction approaches on TinyML hardware deployed for illegal logging detection in
Philippine rainforests:

  •  Raw Spectrogram features: Produced exceptional accuracy and efficient
     resource utilisation for the binary classification task (chainsaw vs.
     ambient), making it the preferred choice for resource-constrained environments
     where simplicity of the inference pipeline is paramount.

  •  Mel Filterbank Energy (MFE) features: Demonstrated superior performance on
     real-world acoustic analysis, particularly for the more demanding multiclass
     sound classification task, achieving 84.4% accuracy at 8 kHz and 89.6%
     at 16 kHz sampling rates.

A critical practical finding was that chainsaw sounds could be reliably detected
at distances of up to 20 metres with either feature set on the RP2040
microcontroller. This range is a key parameter for node spacing in any real-world
zone-based deployment.

2.4.5  Neural Architecture Search (NAS) for Automatic Feature Learning

The most recent paradigm shift in acoustic feature learning eliminates hand-
designed features entirely. Ranmal et al. (2024) proposed ESC-NAS, a hardware-
aware neural architecture search framework that automatically designs deep CNN
architectures to extract features directly from raw audio waveforms. Using black-
box Bayesian optimisation, ESC-NAS explored a cell-based architecture search space
of 2D convolution, batch normalisation, and max-pooling layers, evaluating each
candidate architecture under actual hardware simulation constraints. The resulting
models achieved 85.78% accuracy on the FSC22 dataset, 81.0% on ESC-50, and
96.25% on ESC-10, with model footprints small enough for microcontroller deployment.
The FSC22 dataset, which contains 27 forest-specific sound classes recorded in
real outdoor environments, is particularly relevant to this thesis.


─────────────────────────────────────────────────────────────────────────────────

2.5  MACHINE LEARNING CLASSIFIERS: FROM RANDOM FORESTS TO TINY TRANSFORMERS

The literature on acoustic classification for forest surveillance reveals a clear
evolutionary trajectory, from lightweight classical algorithms on constrained
microcontrollers to hardware-optimised deep neural networks that match or exceed
classical performance with significantly more representational capacity.

2.5.1  Classical Machine Learning: kNN, SVM, and Random Forests

For low-dimensional feature vectors (e.g., 13-coefficient MFCCs or 10-coefficient
LPC vectors), classical classifiers provide competitive baselines with very low
inference latency and memory footprints, making them attractive for the most
constrained hardware.

Singh et al. (2024) compared k-Nearest Neighbours (kNN), Decision Trees (DT),
Random Forests (RF), AdaBoost, and SVMs on their STHT-spectrogram features. Random
Forests provided the best overall balance of accuracy (96.61%), sensitivity
(96.20%), specificity (99.14%), and F-score (96.07%) across five illegal logging
sound classes: chainsaw, hammering, human activity, electric saw, and ambient noise.
Grama and Rusu (2017) similarly found Random Forests superior for LPC-based
wildlife intruder classification (99.25% accuracy), establishing RF as the go-to
classical baseline for acoustic surveillance tasks.

2.5.2  Depthwise-Separable CNNs for Microcontrollers

Standard 2D convolutional layers applied to Mel-Spectrogram inputs produce highly
accurate models but require prohibitive numbers of multiply-accumulate operations
(MACs) for microcontroller inference. Depthwise-Separable Convolutions (DS-Conv),
first widely popularised in MobileNet, decompose a standard 3×3 convolution into:

  1.  A depthwise convolution — one filter per input channel, applied spatially.
  2.  A pointwise convolution — 1×1 convolution across channels.

This decomposition reduces the total number of MACs by a factor of approximately
8–9× compared to standard convolutions, with only a modest accuracy penalty.
Nordby (2019) demonstrated that a DS-CNN designed under a strict 50% resource
budget (CPU, RAM, Flash) on an STM32L476 microcontroller achieved 70.9% accuracy
on UrbanSound8K while using only 20% CPU capacity. This work established the
baseline for subsequent microcontroller audio classification research and validated
that deep learning-quality inference is achievable at the edge.

2.5.3  Tiny Transformers with Attention Mechanisms

Elliott et al. (2021) challenged the dominance of CNNs in edge audio classification
by adapting BERT-style attention mechanisms for the environmental sound domain.
The proposed Tiny Transformer used Mel-Spectrograms as a sequence of time-frequency
patches, processed through multi-head self-attention layers. Despite its drastically
reduced parameter count — approximately 6,000 parameters, compared to over 4 million
for a standard ResNet-18 — the Tiny Transformer outperformed MFCC-based CNN
baselines on an office sound classification dataset.

The critical insight from Elliott et al. (2021) is architectural: self-attention
captures long-range temporal dependencies in the spectrogram (e.g., the slow ramp-
up of a chainsaw engine or the reverberant tail of a gunshot), which are missed by
local convolution kernels. For illegal forest activity classification, where the
temporal structure of sounds is highly discriminative (a continuous chainsaw has
very different temporal dynamics than an impulsive gunshot), self-attention may
provide significant advantages over purely convolutional architectures.

2.5.4  Multi-System Score Fusion

Park et al. (2018) demonstrated that combining the output probability scores of
multiple independent classification systems — each trained on a different feature
set — via a weighted linear fusion significantly improves final accuracy and
robustness. Their system achieved 4th rank in DCASE 2016 through this ensemble
fusion strategy. For the proposed system, where multiple feature streams (MFCC,
MFE, raw spectrogram) may be computed in parallel, late fusion of their
classification scores offers a low-cost path to improved robustness without
requiring a more complex model architecture.


─────────────────────────────────────────────────────────────────────────────────

2.6  IOT HARDWARE, WIRELESS COMMUNICATION, AND ENERGY HARVESTING

2.6.1  Microcontroller Platforms for TinyML Acoustic Systems

The choice of microcontroller directly constrains all other system design decisions,
as it determines the available RAM (for feature computation and model weights),
Flash storage (for the model and firmware), CPU speed (for inference latency), and
power consumption (for battery life). The following platforms are most relevant to
this research:

  •  ESP32 Series (Espressif): Dual-core 240 MHz Xtensa LX6 processor with 520 KB
     SRAM, Wi-Fi and Bluetooth radio, deep-sleep current of ~10 μA. The ESP32-S3
     variant adds vector instructions that accelerate neural network inference.
     Shah et al. (2024) demonstrated adversarial attack transferability specifically
     on ESP32 hardware, confirming it as the de-facto standard for edge audio
     research in cost-sensitive deployments.

  •  RP2040 (Raspberry Pi Foundation): Dual-core ARM Cortex-M0+ at 133 MHz with
     264 KB SRAM. Lorenzo et al. (2024) deployed TinyML models for chainsaw
     detection on the RP2040, achieving 89.6% accuracy at 16 kHz. Its extremely
     low cost and open-source toolchain make it attractive for large-scale
     deployments.

  •  STM32L476 (STMicroelectronics): 80 MHz ARM Cortex-M4F with 96 KB SRAM and
     hardware FPU. Nordby (2019) used this platform as the primary evaluation
     target for CNN-based environmental sound classification, demonstrating that
     depthwise-separable CNNs can run at real-time inference speeds within a
     20% CPU budget.

The ESP32 is selected as the primary platform for this thesis due to its combination
of sufficient processing power for CNN inference, integrated I2S digital
microphone support (for the INMP441 MEMS microphone), deep-sleep power management,
and wide availability at low cost.

2.6.2  Wireless Communication Protocols for Deep Forest Deployment

Selecting the appropriate wireless technology for alert transmission is a
fundamental engineering trade-off between range, power consumption, data rate,
and infrastructure requirements.

  •  LoRaWAN: Singh et al. (2024) integrated a LoRa radio module with their
     intelligent acoustic sensor node, transmitting compressed alert packets
     several kilometres to an internet-connected gateway without requiring any
     cellular infrastructure. LoRaWAN's sub-GHz frequencies (typically 868 MHz
     in Europe, 915 MHz in North America and Asia) penetrate dense forest foliage
     with significantly less attenuation than 2.4 GHz Wi-Fi or Bluetooth signals.
     Papán et al. (2012) similarly designed a WSN for forest monitoring using
     LoRa-compatible radio technologies for chainsaw detection alerts. The key
     limitation is the maximum payload size (~50 bytes for maximum range settings)
     and duty cycle restrictions imposed by regional frequency regulations.

  •  ZigBee (IEEE 802.15.4): Ponniran et al. (2024) demonstrated a ZigBee-based
     forest monitoring WSN optimised for energy efficiency, stability, and
     reliability. ZigBee mesh networking allows alerts to hop between intermediate
     sensor nodes, extending coverage without requiring gateway infrastructure.
     However, its 2.4 GHz operating frequency results in significantly greater
     foliage attenuation than LoRaWAN.

  •  GSM/2G (SIM800L): For deployments in areas with existing cellular coverage
     (common at forest edges and in many tropical regions), a GSM module can
     transmit structured SMS or GPRS data packets directly to a monitoring
     centre. The SIM800L module (as proposed in this thesis) supports AT command
     SMS transmission with a payload of up to 160 characters in standard SMS
     format, sufficient to encode zone ID, detected threat class, confidence
     score, GPS coordinates, and battery status. The key trade-off is higher
     power consumption during transmission (~200 mA peak vs. ~20 mA for LoRa).

  •  LoRaWAN vs. GSM Comparison (Raju et al., 2023): The Green IoT Framework
     for Deep Forest Surveillance evaluated both Wi-Fi (for short-range hub-to-
     base communication) and LoRaWAN (for long-range forest edge transmission)
     in conjunction with an Arduino Nano control board and a NodeMCU gateway,
     concluding that LoRaWAN was superior for deep forest (>500 m from gateway)
     deployments while Wi-Fi or GSM sufficed at forest edges with existing
     cellular coverage.

2.6.3  Energy Harvesting and Power Budget Optimisation

Autonomous long-term deployment in remote forests requires energy harvesting to
supplement or replace battery power. Solar energy harvesting is the most practical
option in tropical and subtropical forest environments where the canopy is not
completely closed. The system design must balance:

  1.  Average power draw of the sensor node (including microcontroller sleep,
      microphone, and radio).
  2.  Solar panel output under forest canopy shading conditions.
  3.  Battery capacity required to bridge multi-day cloudy periods.

Merenda et al. (2020) reviewed edge machine learning techniques for IoT devices
and identified duty-cycling — periodic alternation between deep sleep and active
inference states — as the single most effective strategy for extending battery life.
A typical duty cycle of 10% (e.g., 6 seconds active inference per minute) can
reduce average power consumption from tens of milliamperes to hundreds of
microamperes, enabling weeks of autonomous operation on a single 18650-format
lithium cell.

The proposed system targets a 20 mA average current draw at 5V (100 mW average
power), achievable with a 5W solar panel charging a 2600 mAh LiFePO4 battery
through a TP4056-based charge controller. Under 1 hour of direct sunlight equivalent
per day (a conservative estimate for a forest-edge deployment), this yields
approximately 1.5× daily energy surplus, providing a comfortable buffer for
extended cloudy periods.


─────────────────────────────────────────────────────────────────────────────────

2.7  GUNSHOT AND CHAINSAW ACOUSTIC SIGNATURES: PHYSICAL AND SPECTRAL PROPERTIES

2.7.1  Gunshot Acoustic Signatures for Poaching Detection

Gunshots are the primary acoustic indicator of poaching activity. Their acoustic
signature is produced by two overlapping physical phenomena (Shah et al., 2025):

  1.  The muzzle blast: a high-amplitude broadband impulse generated by the rapid
      expansion of propellant gases. It contains energy across a wide frequency
      range (20 Hz – 20 kHz) with a characteristic fast rise time and exponential
      decay.
  2.  The ballistic shockwave (for supersonic projectiles): a cone-shaped pressure
      wave produced by the projectile travelling faster than the speed of sound.
      It arrives at the sensor after the muzzle blast, with a temporal offset
      proportional to the sensor's distance and angle from the shot trajectory.

Shah et al. (2025) trained CNN and SVM models on 3,459 gunshot recordings from
28 different firearms across 16 calibres (from the Certus Caliber Classification
Gunshot Dataset, C3GD, described by Gurny and Quinn, 2026) and found that the
deep CNN achieved a mean average precision (mAP) of 0.58 on clean field-recorded
data, outperforming the SVM baseline (mAP 0.39). However, models trained on web-
scraped gunshot audio dropped to mAP 0.35 when tested on field recordings,
highlighting the severe quality mismatch between internet-sourced training data
and real-world deployment conditions.

The C3GD dataset (Gurny & Quinn, 2026) directly addresses this data quality problem.
With over 8,000 field-collected recordings from 28 firearms across 16 calibres, at
multiple microphone distances and orientations, it is the most comprehensive and
rigorously labelled gunshot dataset publicly available. Its metadata includes
firearm model, calibre, cartridge type, microphone distance, and environmental
conditions, making it directly applicable to training a robust multi-class poaching
detection model.

Calhoun et al. (2021) extended gunshot detection to the problem of acoustic
multilateration — estimating the shooter's position from the time-of-arrival
differences of the muzzle blast at multiple sensor nodes. Using an algorithm due to
Mathias, Leonari, and Galati under a two-dimensional geometric constraint, their
live-fire tests of the ShotSpotter system in Pittsburgh achieved gunshot location
accuracy of ≤15 metres for 96% of shots when six or more sensors participated.
This multi-node localisation capability is architecturally compatible with the
proposed zone-based deployment described in this thesis: each zone's cluster of
sensors can cooperatively estimate the shot origin within the zone.

Park et al. (2022), through the BGG in-game gunshot dataset, proposed using
synthetic data from first-person shooter (FPS) video games as a supplement for
training gunshot classification and localisation models, demonstrating that game-
engine audio can transfer to real-world classification with improved accuracy.
This data augmentation strategy could be valuable for expanding the training corpus
for rare firearm types in the proposed dataset.

2.7.2  Chainsaw and Mechanical Tool Acoustic Signatures

Chainsaw sounds have a distinctive acoustic signature: a narrow-band tonal component
at the fundamental engine frequency (typically 50–100 Hz, with harmonics up to 1
kHz), combined with a broadband cutting noise from the chain-bar-wood interaction
(1–8 kHz). This combination makes chainsaws relatively easy to detect at moderate
distances but harder to distinguish from other rotating-engine sounds (motorcycles,
generators) as distance increases.

Papán et al. (2012) were among the first to propose autocorrelation-based chainsaw
detection in a WSN context, exploiting the strong periodicity of the engine
fundamental frequency. More recent approaches use spectral features and deep
learning to capture the full harmonic structure.

Singh et al. (2024) validated their STHT-spectrogram + Random Forest system in a
laboratory environment by regenerating chainsaw, hammering, human activity,
electric saw, and ambient noise sounds through loudspeakers, achieving 96.61%
accuracy. The limitation of this validation approach — loudspeaker-based indoor
testing — is that it does not capture the frequency-dependent attenuation and
scattering effects of dense forest foliage, which acts as a low-pass filter that
progressively removes high-frequency chainsaw harmonics with distance. This thesis
addresses this gap through outdoor field validation experiments.

Lorenzo et al. (2024) tested their TinyML chainsaw detection system directly in
Philippine rainforests, confirming reliable detection at up to 20 metres. Beyond
this range, detection rates dropped significantly due to foliage attenuation,
suggesting that node spacing in a zone-based deployment should not exceed 40 metres
(to ensure overlapping coverage between adjacent nodes at their detection limits).


─────────────────────────────────────────────────────────────────────────────────

2.8  DRONE AND UAV-BASED FOREST SURVEILLANCE: COMPLEMENTARY APPROACHES

While this thesis focuses on static sensor node deployments, the drone-based
surveillance literature provides important complementary insights into mission
requirements, acoustic payload design, and detection range benchmarks.

Badea et al. (2024) designed a hybrid VTOL fixed-wing UAV specifically for chainsaw
signature detection and deforestation location reporting. The drone's key design
parameters — a cruise speed of ~50 km/h and a flight autonomy exceeding 3 hours —
were determined by optimising aerodynamic efficiency using fibre-reinforced polymer
composites and thrust-vectoring for hover-to-cruise transition. An onboard
dedicated sound detection system was integrated to identify chainsaw signatures.
The study's relevance to this thesis is methodological: the comparative analysis
of multi-rotor vs. fixed-wing configurations mirrors the trade-off between static
node deployments (which offer permanent coverage but limited area) and mobile UAV
platforms (which offer broader coverage but are subject to battery constraints and
weather conditions). A hybrid deployment combining static acoustic sensor nodes for
continuous perimeter monitoring with periodic UAV patrols for site verification
represents a promising integrated system architecture.

Gül et al. (using an IVN EDAS multi-criteria decision-making framework) evaluated
14 criteria for drone selection in forest fire surveillance, finding that visual
capabilities, diagnosis range, and flight endurance were the most critical factors.
The Barmpoutis et al. (2023) study on Suburban Forest Fire Risk Assessment using
360-degree cameras and a multiscale deformable transformer achieved an F-score of
91.6% for real fire event detection, demonstrating the power of wide-angle sensor
fusion for perimeter monitoring — a concept that directly parallels the multi-
directional microphone array design in this thesis's sensor node enclosure.

Chandana and Vasavi (2022) and Olalekan et al. (2024) both demonstrated drone-
based forest surveillance using Faster R-CNN and deep learning (U-Net, ResNet-50,
InceptionV3) for illegal logging detection from visual imagery. While U-Net achieved
a remarkable 96.8% overall accuracy in detecting logging scars in satellite imagery,
these visual approaches are inherently retrospective — they detect areas already
logged, not the logging event itself. Acoustic detection, as implemented in this
thesis, is prospective and real-time.


─────────────────────────────────────────────────────────────────────────────────

2.9  SYSTEM-LEVEL CHALLENGES AND RESEARCH GAPS

2.9.1  Domain Shift and Hardware Mismatch

A consistent finding across the literature is that models trained on high-quality
studio or internet-sourced audio significantly underperform when deployed with
low-cost MEMS microphones in outdoor enclosures. Zhang et al. (2025) quantified
this domain shift in the DCASE 2024 context and proposed entropy-guided curriculum
learning as a mitigation. Shah et al. (2025) measured a drop from mAP 0.58 to
mAP 0.35 when switching from clean field recordings to web-sourced training data.
Gurny and Quinn (2026) introduced the C3GD dataset to address data quality through
rigorous field collection.

For this thesis, domain shift is mitigated through:
  (a) Field-recording the training dataset using the same INMP441 microphone model
      and outdoor enclosure that will be used in deployment.
  (b) Applying SpecAugment and AddNoise augmentations during training to improve
      robustness to recording device variability.
  (c) Using an entropy-guided curriculum that prioritises device-invariant training
      samples, following Zhang et al. (2025).

2.9.2  Adversarial Robustness in TinyML Systems

Shah et al. (2024) demonstrated a particularly alarming security vulnerability in
TinyML acoustic systems: adversarial perturbations — subtle, precisely crafted noise
patterns imperceptible to human ears — generated on a high-powered host machine can
be transferred directly to ESP32 and Raspberry Pi deployments, causing the model to
misclassify a genuine chainsaw sound as ambient noise or vice versa. In a forest
surveillance context, this means a sophisticated intruder equipped with a smartphone
app could play back an adversarial audio signal to spoof the sensor node and disable
the alert system.

This research gap is not addressed in this thesis's initial prototype, but it
represents a critical direction for future hardening. Potential mitigation strategies
include:
  •  Adversarial training (augmenting the training set with adversarial examples).
  •  Randomised smoothing (adding certified Gaussian noise to inference inputs).
  •  Multi-modal fusion (combining acoustic with secondary sensors — PIR motion,
     vibration — to prevent single-modality spoofing).

2.9.3  Multi-Zone Alert Architecture and Communication Reliability

Singh et al. (2024) demonstrated a zone-to-gateway LoRa alert architecture. Papán
et al. (2012) described early WSN topologies for forest monitoring. However, the
literature contains no published study that specifically addresses a multi-zone
GSM-based alert architecture with structured payload encoding for multiple forest
enforcement agencies (police, coast guard, and forest authority) simultaneously.

Zanella et al. (2014) provided a foundational reference for urban IoT architectures
that can be mapped to the forest context: their Padova Smart City project demonstrated
multi-sensor, multi-gateway IoT deployments with open data access for multiple
stakeholder services. Adapting this architecture to the forest domain — with GSM
as the wide-area network layer and a cloud-hosted alert management dashboard as
the control plane — represents the novel system contribution of this thesis.

2.9.4  Dataset Scarcity for Multi-Class Forest Illegal Activity Detection

The literature reveals a critical gap in publicly available, richly labelled,
outdoor-recorded datasets covering the full range of illegal forest activity sounds:
gunshots, multiple chainsaw models, axe chopping, vehicle engines, human voices
(in multiple languages), and ambient forest soundscapes (with wind, rain, and
birdsong variations). ESC-50 provides 50 environmental sound classes (Lorenzo et
al., 2024; Ranmal et al., 2024), but only a subset is relevant to forest surveillance.
FSC22 was specifically designed for forest sounds (27 classes) and represents the
closest existing dataset to the requirements of this thesis.

The proposed system addresses this gap by constructing a custom dataset combining:
  •  Existing publicly available recordings from ESC-50, FSC22, UrbanSound8K,
     and the C3GD gunshot dataset.
  •  Field recordings collected specifically for this project using the INMP441
     microphone and the final sensor node enclosure design.
  •  Synthetically augmented samples generated through SpecAugment, RoomSimulator,
     and controlled distance simulation (applying inverse-square-law attenuation
     and frequency-dependent atmospheric absorption).


─────────────────────────────────────────────────────────────────────────────────

2.10  SUMMARY AND POSITIONING OF THIS RESEARCH

Table 2.1 provides a concise summary of the most closely related existing systems,
comparing them against the system proposed in this thesis.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

System                  MCU          Comms    Features  Classes   Acc.    Zones
─────────────────────────────────────────────────────────────────────────────────
Singh et al. (2024)     32-bit MCU   LoRa     STHT      5        96.61%   No
Lorenzo et al. (2024)   RP2040       None     MFE/Spec  2        89.6%    No
Nordby (2019)           STM32L476    None     Mel-Spec  10       70.9%    No
Elliott et al. (2021)   MCU (sim.)   None     Mel-Spec  env.snd  >CNN    No
Ranmal et al. (2024)    ESP32-S3     None     Raw Audio 27       85.78%   No
Papán et al. (2012)     WSN node     LoRa     Autocorr. 1        N/A      No
Grama & Rusu (2017)     PC (sim.)    None     LPC       5        99.25%   No
─────────────────────────────────────────────────────────────────────────────────
THIS THESIS             ESP32        GSM      MFCC+MFE  10+      >90%    YES
                        (Solar)      (SIM800L)(ensemble)         target  Multi-
                        powered                                           zone
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Table 2.1: Comparison of existing TinyML acoustic forest surveillance systems
against the proposed system.

The table reveals the key research contributions of this thesis:

  1.  Multi-class illegal activity detection (10+ target classes vs. 1–5 in
      prior work) integrating chainsaws, gunshots, vehicles, and human voices
      in a single unified model.

  2.  Multi-zone alert architecture with GSM transmission, delivering structured
      alert payloads (zone ID, detected class, confidence, GPS coordinates,
      battery status) to multiple enforcement authorities simultaneously.

  3.  Solar-powered autonomous operation with optimised duty-cycling, enabling
      indefinite deployment without battery replacement.

  4.  Solar-box enclosure design (IP-rated, Gore-Tex acoustic port, multi-
      directional microphone placement) specifically engineered for tropical
      forest edge conditions.

  5.  Field validation in real forest conditions (rather than laboratory
      loudspeaker simulations), directly addressing the domain-shift challenge
      identified by Zhang et al. (2025) and Shah et al. (2025).

The following chapters describe the system design, dataset construction, model
training, hardware implementation, and field evaluation procedures that realise
these contributions.


─────────────────────────────────────────────────────────────────────────────────

REFERENCES (Chapter 2)

Ali, G., Mıjwıl, M. M., Adamopoulos, I., & Ayad, J. (2025). Leveraging the
  Internet of Things, Remote Sensing, and Artificial Intelligence for Sustainable
  Forest Management. Babylonian Journal of Internet of Things, 2025(1).
  https://doi.org/10.58496/bjiot/2025/001

Badea, G., Frigioescu, T., Dombrovschi, M., Cican, G., Dima, M., Anghel, V., &
  Crunțeanu, D. (2024). Innovative Hybrid UAV Design, Development, and Manufacture
  for Forest Preservation and Acoustic Surveillance. Semantic Scholar.

Barmpoutis, P., Kastridis, A., Stathaki, T., Yuan, J., Shi, M., & Grammalidis, N.
  (2023). Suburban Forest Fire Risk Assessment and Forest Surveillance Using
  360-Degree Cameras and a Multiscale Deformable Transformer. Semantic Scholar.

Calhoun, R. B., Dunson, C., Johnson, M. L., Lamkin, S. R., Lewis, W. R., Showen,
  R. L., Sompel, M. A., & Wollman, L. P. (2021). Precision and accuracy of acoustic
  gunshot location in an urban environment. arXiv:2108.07377.

Chandana, V., & Vasavi, S. (2022). Autonomous drones based forest surveillance
  using Faster R-CNN. Semantic Scholar.

Duppada, V., & Hiray, S. (2017). Ensemble of Deep Neural Networks for Acoustic
  Scene Classification. arXiv:1708.05826.

Elliott, D., Otero, C. E., Wyatt, S., & Martino, E. (2021). Tiny Transformers for
  Environmental Sound Classification at the Edge. arXiv:2103.12157.
  https://doi.org/10.48550/arxiv.2103.12157

Grama, L., & Rusu, C. (2017). Audio signal classification using Linear Predictive
  Coding and Random Forests. Proceedings of SpeD 2017.
  https://doi.org/10.1109/sped.2017.7990431

Gurny, S., & Quinn, R. (2026). Descriptor: Certus Caliber Classification Gunshot
  Dataset (C3GD). arXiv:2606.18135.

Gül, A. Y., Çakmak, E., & Karakas, A. E. (n.d.). Drone Selection for Forest
  Surveillance and Fire Detection Using Interval Valued Neutrosophic EDAS Method.

Innes, J. L. (2010). Madagascar rosewood, illegal logging and the tropical timber
  trade. Madagascar Conservation & Development, 5(1).
  https://doi.org/10.4314/mcd.v5i1.57335

Johnson, L. K., Mahoney, M. J., Desrochers, M. L., & Beier, C. M. (2023). Mapping
  historical forest biomass for stock-change assessments at parcel to landscape
  scales. arXiv:2303.04538.

Lorenzo, A., Barien, R., Favila, N. D., Basa, D., Ventura, J. M., & Catolos, S. N.
  (2024). Trees have Ears: An Acoustic Surveillance and TinyML-Based System for
  Detecting Illegal Logging. Semantic Scholar.

Merenda, M., Porcaro, C., & Iero, D. (2020). Edge Machine Learning for AI-Enabled
  IoT Devices: A Review. Sensors, 20(9), 2533.
  https://doi.org/10.3390/s20092533

Nordby, J. (2019). Environmental sound classification on microcontrollers using
  Convolutional Neural Networks. Norwegian University of Life Sciences. Open Access.
  http://hdl.handle.net/11250/2611624

Olalekan, J., Kile, S., & Bassi, J. (2024). Development of an intelligent forest
  surveillance and analytics system. PubMed.

Papán, J., Jurecka, M., & Púchyová, J. (2012). WSN for forest monitoring to prevent
  illegal logging. FedCSIS 2012.

Park, J., Cho, Y., Sim, G., Lee, H., & Choo, J. (2022). Enemy Spotted: in-game gun
  sound dataset for gunshot classification and localization. arXiv:2210.05917.

Park, S., Mun, S., Lee, Y., Han, D. K., & Ko, H. (2018). Analysis Acoustic Features
  for Acoustic Scene Classification and Score fusion of multi-classification systems
  applied to DCASE 2016 challenge. arXiv:1807.04970.

Ponniran, A., Vajravelu, A., Zaki, W., Yamunarani, T., Ahammed, S., & Sivaranjani,
  S. (2024). IoT/WSN-based Security/privacy Methods for Forest Monitoring.
  Semantic Scholar.

Raju, P., Lakshmi Priya, S., Ksheeraja, S., Menaga, B., & Ragul, V. (2023). Green
  IoT Framework for Deep Forest Surveillance. Semantic Scholar.

Ranmal, D., Ranasinghe, P., Paranayapa, T., Meedeniya, D., & Perera, C. (2024).
  ESC-NAS: Environment Sound Classification Using Hardware-Aware Neural Architecture
  Search for the Edge. Sensors, 24(12), 3749.
  https://doi.org/10.3390/s24123749

Saim, A., & Aly, M. H. (2025). Fusion-Based Approaches and Machine Learning
  Algorithms for Forest Monitoring: A Systematic Review. Semantic Scholar.

Sethi, S. S., Jones, N. S., Fulcher, B., Picinali, L., Clink, D. J., Klinck, H.,
  Orme, C. D. L., Wrege, P. H., & Ewers, R. M. (2020). Characterizing soundscapes
  across diverse ecosystems using a universal acoustic feature set. Proceedings of
  the National Academy of Sciences, 117(29).
  https://doi.org/10.1073/pnas.2004702117

Shah, A., Singh, R., Raj, B., & Hauptmann, A. (2025). Deciphering GunType Hierarchy
  through Acoustic Analysis of Gunshot Recordings. arXiv:2506.20609.

Shah, P., Govindarajulu, Y., Kulkarni, P., & Parmar, M. (2024). Enhancing TinyML
  Security: Study of Adversarial Attack Transferability. arXiv:2407.11599.

Singh, V., Ray, K. C., & Tripathy, S. (2024). Real-Time Monitoring of Illegal
  Logging Events Using Intelligent Acoustic Sensors Nodes. IEEE Sensors Journal.
  https://doi.org/10.1109/jsen.2024.3419897

Tleimat, J., Fritts, S. R., Brunner, R. M., Rodríguez, D., Lynch, R. L., &
  McCracken, S. F. (2022). Economic pressures of Covid-19 lockdowns result in
  increased timber extraction within a critically endangered region. Ecology and
  Evolution, 12(12). https://doi.org/10.1002/ece3.9550

Xue, Z., Lin, H., & Wang, F. (2022). A Small Target Forest Fire Detection Model
  Based on YOLOv5 Improvement. Semantic Scholar.

Zanella, A., Bui, N., Castellani, A., Vangelista, L., & Zorzi, M. (2014). Internet
  of Things for Smart Cities. IEEE Internet of Things Journal, 1(1), 22–32.
  https://doi.org/10.1109/JIOT.2014.2306328

Zhang, P., Liu, Y., Li, Z., Sang, R., Cai, Y., Tan, Y., & Li, S. (2025).
  An Entropy-Guided Curriculum Learning Strategy for Data-Efficient Acoustic Scene
  Classification under Domain Shift. arXiv:2509.11168.

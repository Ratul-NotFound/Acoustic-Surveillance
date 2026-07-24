# ESC-50 Dataset Contents & Project Class Mapping

The **ESC-50 (Environmental Sound Classification)** dataset is a labeled collection of 2,000 environmental audio recordings. It is widely used as an academic benchmark for evaluating environmental sound classification models.

---

## 1. Dataset Specifications
*   **Total Audio Clips**: 2,000
*   **Total Classes**: 50 (exactly 40 clips per class)
*   **Clip Duration**: 5 seconds
*   **Original Audio Format**: 44.1 kHz, Mono, 16-bit Ogg Vorbis/WAV
*   **Dataset Structure**: Organized into 5 cross-validation folds to help you evaluate model accuracy without overfitting.

---

## 2. The 50 Labeled Classes (Categorized)

The 50 classes are divided into 5 distinct environmental categories:

### A. Animals (10 Classes)
*   Dog (barks)
*   Rooster
*   Pig
*   Cow
*   Frog
*   Cat
*   Hen
*   Insects (cicadas)
*   Sheep
*   Crow

### B. Natural Soundscapes & Water (10 Classes)
*   Rain
*   Sea waves
*   Crackling fire
*   Crickets
*   Chirping birds
*   Water drops
*   Wind
*   Pouring water
*   Demolition
*   Gushing water

### C. Human, Non-Speech Sounds (10 Classes)
*   Crying
*   Sneezing
*   Laughter
*   Snoring
*   Coughing
*   Footsteps
*   Yawning
*   Finger snapping
*   Clapping
*   Breathing

### D. Domestic / Home Sounds (10 Classes)
*   Door knock
*   Mouse click
*   Keyboard typing
*   Door, wood creaks
*   Can opening
*   Washing machine
*   Vacuum cleaner
*   Clock ticking
*   Glass breaking
*   Clock alarm

### E. Urban & Mechanical Noises (10 Classes)
*   Helicopter
*   Chainsaw
*   Siren
*   Car horn
*   Engine (truck/car)
*   Train
*   Church bells
*   Airplane
*   Fireworks
*   Handgun

---

## 3. Direct Mapping to Your 31 Forest Surveillance Classes

ESC-50 directly covers **12 of your target classes** out-of-the-box. You can extract these folders to populate your dataset instantly:

| Your Forest Surveillance Class | Matching ESC-50 Class | Description in ESC-50 |
| :--- | :--- | :--- |
| **Chainsaw** | `chainsaw` | Gas-powered 2-stroke chainsaw operating |
| **Gunshot** | `handgun` | Dry, high-energy pistol fire shots |
| **Footsteps** | `footsteps` | Rhythmic human footsteps walking |
| **Hunting Dog** | `dog` | Domestic canine barks and howling |
| **Campfire Crackle** | `crackling_fire` | Logs burning, popping, and sizzling |
| **Rain (Light/Heavy)** | `rain` | Rushing rain droplets falling on surfaces |
| **Wind (Canopy/Gusts)** | `wind` | Howling gusts and tree movement noise |
| **Bird Calls/Songs** | `chirping_birds` | High-pitched bird songs and chirps |
| **Cicadas / Insect Hums** | `insects` / `crickets` | Continuous high-frequency insect vibrations |
| **Frog Croaks** | `frog` | Pulsed croaking calls |
| **River / Stream Flowing** | `gushing_water` / `water_drops` | Running river/water stream soundscapes |
| **Vehicle Engines** | `engine` | Continuous diesel/gasoline vehicle motor hums |
 Pregenerated folders for other sounds can be safely ignored or deleted.

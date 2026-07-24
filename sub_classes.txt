# Thesis Taxonomy: Deep Acoustic Sub-Class Analysis

A major challenge in forest acoustic monitoring is **intra-class variance**—the fact that different models, calibers, or materials under the same category sound completely different. 

To build a high-performance TinyML model, you must recognize these sub-classes during dataset assembly and training. This document details the acoustic variations and spectral signatures of your core threat sub-classes.

---

## 1. Chainsaw Sub-Classes

Chainsaws vary significantly based on their power source (gasoline vs. electric/battery).

### Sub-Class A: Gasoline 2-Stroke Chainsaw (Classic)
*   **Acoustic Signature**: Raspy, erratic, combustion-dominated harmonics.
*   **Spectral Characteristics**: Rich low-frequency harmonics (\(80\text{ Hz} - 500\text{ Hz}\)) representing cylinder explosions. When cutting, the RPMs sag and the pitch drops under load, creating a weeping sound.
*   **Inference Impact**: High low-frequency energy. Needs a low-pass or wideband filter config.

### Sub-Class B: Electric / Battery Chainsaw (Modern)
*   **Acoustic Signature**: High-pitched coil whine, whistling fan noise, clean hum.
*   **Spectral Characteristics**: Absence of low-frequency engine pops. Dominated by high-frequency electric motor PWM switching and gearing sounds (\(1\text{ kHz} - 4\text{ kHz}\)). RPMs remain highly stable even under load.
*   **Inference Impact**: Can be easily missed if your model relies too heavily on low-frequency engine signatures. High-frequency bins must be weighted properly.

---

## 2. Chopping & Clearing Sub-Classes

Chopping sounds vary based on the wood density and the tool being used.

### Sub-Class A: Steel Axe on Hardwood
*   **Acoustic Signature**: Bright metallic ring followed by a clean, sharp crack.
*   **Spectral Characteristics**: Sharp impact transient (<10ms rise time) with a distinct metallic resonance ring (\(1.5\text{ kHz} - 3\text{ kHz}\)) from the steel head.
*   **Inference Impact**: Very easy to detect due to the high-frequency metal ring component.

### Sub-Class B: Steel Axe on Softwood / Wet Wood
*   **Acoustic Signature**: Dull, muffled "thud".
*   **Spectral Characteristics**: Low-to-mid frequency compression (\(100\text{ Hz} - 800\text{ Hz}\)) with almost no high-frequency steel resonance. The decay is very short as wet/soft wood absorbs the sound waves.
*   **Inference Impact**: Harder to detect. Often misclassified as large animal footsteps or dropping branches.

### Sub-Class C: Machete / Brush Hook on Bamboo & Undergrowth
*   **Acoustic Signature**: Rhythmic swishing followed by light, hollow cracking sounds.
*   **Spectral Characteristics**: Broad high-frequency friction noise (\(2\text{ kHz} - 6\text{ kHz}\)) from the blade moving through air/leaves, followed by a hollow impulse.
*   **Inference Impact**: Rhythmic and lower energy than axe chopping.

---

## 3. Gunshot Sub-Classes (Poaching)

Gunshots differ based on bullet speed (supersonic vs. subsonic) and caliber.

### Sub-Class A: Supersonic Rifle (e.g., .223, 7.62mm, Hunting Rifles)
*   **Acoustic Signature**: Dual-event "Crack-Bang".
*   **Spectral Characteristics**: 
    1. A sharp, high-frequency bow-shockwave "crack" (caused by the bullet breaking the sound barrier, peaks at \(3\text{ kHz} - 8\text{ kHz}\)).
    2. A slightly delayed muzzle blast "bang" (lower frequency, \(100\text{ Hz} - 500\text{ Hz}\)).
*   **Inference Impact**: Extremely loud and distinct. Easy to classify even at long distances.

### Sub-Class B: Subsonic Handgun (e.g., 9mm, .45 ACP, Pistols)
*   **Acoustic Signature**: Single-event "Pop" or "Bang".
*   **Spectral Characteristics**: Muzzle blast only (no supersonic shockwave). Lower energy, with a broader frequency distribution (\(100\text{ Hz} - 2\text{ kHz}\)).
*   **Inference Impact**: Decays much faster with distance than rifle fire.

### Sub-Class C: Shotgun (e.g., 12-Gauge)
*   **Acoustic Signature**: Heavy, bass-heavy booming blast.
*   **Spectral Characteristics**: Huge low-frequency pressure wave (\(30\text{ Hz} - 400\text{ Hz}\)) with a long acoustic decay. High amplitude over a wide area.
*   **Inference Impact**: Can saturate/clip the microphone if fired nearby, causing flat-top wave clipping.

### Sub-Class D: Air Rifle / Pneumatic Gun (Silent Poaching)
*   **Acoustic Signature**: Short, metallic pop and hiss.
*   **Spectral Characteristics**: Very low amplitude. High-frequency pneumatic exhaust hiss (\(2\text{ kHz} - 6\text{ kHz}\)).
*   **Inference Impact**: Very quiet; requires the sensor node to be closer to the source to detect.

---

## 4. Boat Sub-Classes (River Forests / Floodplain Logging)

Boats are the primary transport for illegal logging in delta/river forests.

### Sub-Class A: Long-tail Boat (Unmuffled 2/4-Stroke)
*   **Acoustic Signature**: Deafening, metallic, rapid mechanical popping.
*   **Spectral Characteristics**: Extremely loud. Exhaust discharges directly into the air. Features sharp, rhythmic engine pulses (\(50\text{ Hz} - 600\text{ Hz}\)) that echo off river banks.
*   **Inference Impact**: Very high amplitude. Dominates the acoustic landscape; easy to detect from miles away.

### Sub-Class B: Outboard Motorboat (Muffled)
*   **Acoustic Signature**: Continuous low-frequency hum, bubbling, water cavitation.
*   **Spectral Characteristics**: Exhaust is muffled underwater. High-frequency water bubbling and propeller shearing noise (\(1\text{ kHz} - 5\text{ kHz}\)) mixed with a steady low motor hum.
*   **Inference Impact**: Moderately quiet; sound is directional and absorbed by water.

### Sub-Class C: Manual Paddling / Oar Rowing
*   **Acoustic Signature**: Rhythmic splashing and creaking.
*   **Spectral Characteristics**: Low-amplitude periodic splashing (\(500\text{ Hz} - 3\text{ kHz}\)) coupled with wood-on-wood creaking of the oarlocks.
*   **Inference Impact**: Extremely quiet. Requires temporal pattern matching over several seconds.

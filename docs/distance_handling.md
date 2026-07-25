# Thesis Guide: Handling Acoustic Distance, Attenuation, & Reverberation

In a real forest deployment, sounds will be recorded at varying distances from the sensor node (from 5 meters to over 500 meters). As sound travels through a dense forest, it undergoes physical transformations that completely alter its acoustic profile.

If your model is only trained on close-up, clean recordings, it will fail to detect distant threats. This guide details how to handle distance-based attenuation, foliage absorption, and multipath reverberation.

---

## 1. The Physics of Forest Acoustic Propagation

When sound travels through a forest, it is degraded by three primary physical processes:

```
[ Close Sound Source ] ──( 6dB Drop per Double Distance )──> [ Geometric Spreading ]
[ Foliage & Leaves ] ──( Absorbs Frequencies > 1kHz )──────> [ High-Frequency Attenuation ]
[ Tree Trunks & Ground ] ──( Multiple Sound Reflections )──> [ Temporal Reverberation ]
```

1.  **Geometric Spreading (Volume Drop)**: Sound energy drops by approximately **6 dB for every doubling of distance** from the source (the Inverse Square Law).
2.  **Excess Attenuation (Foliage Absorption)**: Leaves, pine needles, and undergrowth act as low-pass filters. They absorb high frequencies much faster than low frequencies. Frequencies above **1 kHz** attenuate rapidly over distance.
3.  **Multipath Scattering (Reverberation)**: Sound waves bounce off tree trunks and the forest floor. A clean, sharp sound (like a 10ms gunshot or axe chop) gets scattered, smearing the sound over time into a longer, muddy echo (up to 300ms).

---

## 2. Spectrogram Alteration: Close vs. Distant Sounds

Your TinyML Convolutional Neural Network (CNN) reads Mel-Spectrograms as images. Here is how distance changes those images:

### Example: Gunshot Spectrograms
*   **Close Gunshot (e.g., < 30m)**:
    *   *Visual*: A sharp, dark vertical line spanning from 100Hz to 8,000Hz.
    *   *Amplitude*: High energy, crisp, clear transient start.
*   **Distant Gunshot (e.g., > 300m)**:
    *   *Visual*: A blurry, faint blob restricted entirely to low frequencies (under 800Hz) with a long tail.
    *   *Amplitude*: Very low energy, low Signal-to-Noise Ratio (SNR).

---

## 3. Machine Learning Solutions (Data Augmentation)

To make your TinyML model capable of recognizing both close and distant sounds, you must apply **Data Augmentation** to your dataset in Python before training:

### Python Augmentation Strategy
When compiling your training data, take your close-up recordings (e.g., clean chainsaw or gunshot clips) and programmatically generate "distant" versions using these transformations:

1.  **Gain Reduction (Volume Control)**:
    *   Scale the amplitude of the audio array by a random factor between `0.05` and `0.3` to simulate volume drop.
2.  **Low-Pass Filtering (Foliage Simulation)**:
    *   Apply a Butterworth low-pass filter with a random cutoff frequency between `500 Hz` and `1.5 kHz` to simulate leaf absorption.
3.  **Reverberation (Multipath Simulation)**:
    *   Convolve the audio with a synthetic room impulse response (RIR) or add a decay echo to simulate scattering off tree trunks.
4.  **Noise Injection (SNR Degradation)**:
    *   Mix the clean sound with a continuous recording of forest background wind/rain at varying Signal-to-Noise Ratios (from +15dB down to -5dB).

---

## 4. Software Solutions in ESP32-S3 Firmware

On the microcontroller, you must implement techniques to ensure faint signals are not ignored and loud signals do not distort (clip) the analog-to-digital converter (ADC).

### Technique A: Logarithmic Spectrogram Scaling
When configuring your feature extractor (MFE block in Edge Impulse), ensure you use **Logarithmic Scaling**:
$$\text{Output} = 10 \cdot \log_{10}(\text{Mel Energy})$$
*   *Why*: Human hearing and sound propagation are logarithmic. Log-scaling compresses loud, close-up sounds while boosting the contrast of quiet, distant sounds, allowing the neural network to analyze both on the same scale.

### Technique B: Software Digital Automatic Gain Control (AGC)
If your digital microphone does not have hardware AGC, you can implement a simple software gain-scaling step in your ESP32 C++ buffer before running inference:

```cpp
void apply_digital_agc(int16_t* buffer, size_t size, float target_rms = 4000.0) {
  float sum = 0.0;
  
  // 1. Calculate the Root Mean Square (RMS) volume of the current 2s block
  for (size_t i = 0; i < size; i++) {
    sum += buffer[i] * buffer[i];
  }
  float rms = sqrt(sum / size);
  
  // 2. If the block is very quiet, boost it dynamically
  if (rms > 50.0 && rms < target_rms) {
    float gain = target_rms / rms;
    if (gain > 8.0) gain = 8.0; // Cap maximum gain boost at 8x to avoid boosting sensor floor noise
    
    for (size_t i = 0; i < size; i++) {
      int32_t boosted = (int32_t)(buffer[i] * gain);
      // Prevent overflow clipping
      if (boosted > 32767) boosted = 32767;
      if (boosted < -32768) boosted = -32768;
      buffer[i] = (int16_t)boosted;
    }
  }
}
```
*Add this function inside your ESP32 sketch right after reading the raw I2S microphone data.*

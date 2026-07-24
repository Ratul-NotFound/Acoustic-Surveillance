# Thesis Guide: Acoustic Data Collection Strategies

Building a high-quality dataset is 80% of the work in an Edge AI / TinyML thesis. To build a robust 31-class classifier, you must combine public datasets, custom web-scraped clips, and custom field recordings.

This guide outlines exactly how and where to collect data for your forest acoustic surveillance system.

---

## 1. Top Public Databases for Forest Acoustics

Using established public datasets ensures your project is academically valid and speeds up the training phase.

### A. Environmental & Threat Sounds
*   **ESC-50 (Environmental Sound Classification)**:
    *   *Where to get*: GitHub or Kaggle.
    *   *Available Classes*: Chainsaw, gunshot, rain, wind, thunder, footsteps, campfire crackle, dog barking.
    *   *Format*: 2,000 5-second clean clips.
*   **Rainforest Connection (RFCx) Open Data**:
    *   *Where to get*: [rfcx.org](https://rfcx.org/) / Kaggle.
    *   *Available Classes*: Real forest ambient noise, rain, wind, animal vocalizations, illegal chainsaw logging, and shotgun fire recorded in actual jungles.
*   **Google AudioSet**:
    *   *Where to get*: [AudioSet Ontology website](https://research.google.com/audioset/).
    *   *Available Classes*: "Handsaw", "Axe", "Wood chopping", "Walkie-talkie", "Heavy machinery", "Drone propellers", "Outboard motorboat".

### B. Biological / Animal Sounds (Wildlife)
*   **Xeno-Canto**:
    *   *Where to get*: [xeno-canto.org](https://xeno-canto.org/).
    *   *Available Classes*: The world's largest open-access database of bird songs, frog croaks, and primate/monkey calls. You can download mp3s of specific species.

---

## 2. Collecting Custom Audio via Web Scraping

If you cannot find clean audio files for specific sub-classes (like custom boat engines or specific walkie-talkie beeps), you can scrape them from YouTube.

I have created a Python script in your workspace at `data_prep/download_youtube.py` that automates this. 

### How to use the Scraper:
1.  Find YouTube videos of the sound you need (e.g., "long-tail boat engine sound", "chainsaw idling").
2.  Add the YouTube URLs to the script.
3.  The script will download the audio, extract the exact segment you want (e.g., from minute 1:00 to 2:00), resample it to `16kHz, mono, WAV`, and save it directly to your raw data directory.

---

## 3. Recording Directly from the ESP32-S3 Hardware (Edge Impulse Daemon)

For the highest accuracy, you should train your model on audio captured by the **exact same microphone** (INMP441) and hardware setup you will deploy. This accounts for the mic’s unique frequency response.

### Method: The Edge Impulse CLI Daemon
Edge Impulse allows you to stream audio directly from your ESP32-S3 to the cloud for automatic labeling and segmenting.

1.  **Install Node.js** on your computer.
2.  Install the Edge Impulse CLI by running in your terminal:
    ```bash
    npm install -g edge-impulse-cli
    ```
3.  Flash the **Edge Impulse Firmware** to your ESP32-S3 (Edge Impulse provides a pre-compiled binary for the ESP32-S3 Eye/Sense board).
4.  Connect the ESP32-S3 to your PC via USB and run:
    ```bash
    edge-impulse-daemon
    ```
5.  Log in to your account. Your ESP32-S3 will appear as a recording device in the **Edge Impulse Studio**.
6.  Click **Record** in the browser. The ESP32-S3 will record, upload, and format the audio automatically.

---

## 4. Generating Synthetic Data (Mixer Augmentation)

In a forest, threats are mixed with background noise. You can synthetically build this in Python.

### The Mixing Recipe:
If you have a clean gunshot recording (\(G\)) and a continuous recording of forest rain (\(R\)):
$$\text{Mixed Sample} = (G \cdot \alpha) + (R \cdot \beta)$$
Where \(\alpha\) and \(\beta\) are gain scales. By varying \(\alpha\) and \(\beta\), you can create 100 different training samples from just 1 gunshot clip, simulating different distances and rain volumes.

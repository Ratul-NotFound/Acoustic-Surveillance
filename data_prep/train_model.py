"""
train_model.py
──────────────
TinyML 2D CNN Model Trainer & C++ Header Exporter for ESP32-S3

Features:
  1. Feature Extraction: Computes 40-band Log-Mel Spectrograms (40 x 49 matrix per 3s clip at 16kHz).
  2. Dataset Caching: Caches features to data_prep/features_26class.npz for fast re-training.
  3. Depthwise-Separable 2D CNN (DS-CNN): Optimized for MCU memory bounds (520KB SRAM).
  4. Train / Val / Test Evaluation: Generates accuracy metrics & confusion matrix.
  5. TFLite INT8 Quantization: Converts trained model to TFLite INT8 format.
  6. C++ Header Export: Writes firmware/model_data.h (byte array ready for ESP32-S3 Arduino sketch).
"""

import os
import sys
import glob
import json
import numpy as np
import soundfile as sf
import librosa

DATASET_DIR = r"E:\software\acoustic-surveillance\data_prep\q1_dataset"
CACHE_FILE = r"E:\software\acoustic-surveillance\data_prep\features_26class.npz"
LABEL_MAP_FILE = r"E:\software\acoustic-surveillance\data_prep\label_map.json"
MODEL_H_FILE = r"E:\software\acoustic-surveillance\firmware\model_data.h"
TFLITE_FILE = r"E:\software\acoustic-surveillance\firmware\model_quantized.tflite"

N_MELS = 40
N_FFT = 1024
HOP_LENGTH = 1024
TARGET_SR = 16000
CLIP_SAMPLES = 48000  # 3 seconds at 16kHz

def extract_features():
    """Scans q1_dataset, extracts 40x49 Log-Mel Spectrograms for all 5,200 WAV files."""
    if os.path.exists(CACHE_FILE):
        print(f"Loading cached features from: {CACHE_FILE}")
        data = np.load(CACHE_FILE)
        return data['X'], data['y'], list(data['classes'])

    print("Extracting Log-Mel Spectrogram features from 5,200 clean WAV files on SSD...")
    classes = sorted([d for d in os.listdir(DATASET_DIR) if os.path.isdir(os.path.join(DATASET_DIR, d))])
    class_to_idx = {cls_name: idx for idx, cls_name in enumerate(classes)}

    X_list = []
    y_list = []

    for cls_name in classes:
        cls_dir = os.path.join(DATASET_DIR, cls_name)
        wav_files = glob.glob(os.path.join(cls_dir, "*.wav"))
        print(f"  Processing '{cls_name}': {len(wav_files)} files...")

        for fpath in wav_files:
            try:
                audio, sr = sf.read(fpath)
                if len(audio.shape) > 1:
                    audio = np.mean(audio, axis=1)

                if sr != TARGET_SR:
                    audio = librosa.resample(audio, orig_sr=sr, target_sr=TARGET_SR)

                if len(audio) < CLIP_SAMPLES:
                    audio = np.pad(audio, (0, CLIP_SAMPLES - len(audio)))
                else:
                    audio = audio[:CLIP_SAMPLES]

                # Compute Mel Spectrogram (40 bands x 49 time frames)
                mel_spec = librosa.feature.melspectrogram(
                    y=audio, sr=TARGET_SR, n_fft=N_FFT, hop_length=HOP_LENGTH, n_mels=N_MELS
                )
                log_mel = librosa.power_to_db(mel_spec, ref=np.max)

                # Normalize features to [0, 1] range
                norm_mel = (log_mel - np.min(log_mel)) / (np.max(log_mel) - np.min(log_mel) + 1e-6)

                X_list.append(norm_mel)
                y_list.append(class_to_idx[cls_name])

            except Exception as e:
                print(f"    Error reading {fpath}: {e}")

    X = np.array(X_list, dtype=np.float32)
    X = np.expand_dims(X, axis=-1)  # Shape: (N, 40, 49, 1)
    y = np.array(y_list, dtype=np.int32)

    # Cache features to disk
    np.savez_compressed(CACHE_FILE, X=X, y=y, classes=np.array(classes))
    with open(LABEL_MAP_FILE, 'w') as f:
        json.dump(class_to_idx, f, indent=2)

    print(f"Feature extraction complete. Shape X: {X.shape}, y: {y.shape}")
    return X, y, classes

def export_c_header(tflite_model_bytes, classes):
    """Exports INT8 quantized TFLite model as a clean C++ header file for ESP32-S3."""
    print(f"\nExporting C++ header to: {MODEL_H_FILE}")

    hex_data = tflite_model_bytes
    lines = []
    lines.append("// ==========================================================================")
    lines.append("// Auto-generated TinyML 2D CNN Model Header for ESP32-S3 Forest Surveillance")
    lines.append(f"// Classes: {len(classes)} | Target SR: 16000Hz | Feature: {N_MELS} Mel Bands")
    lines.append("// ==========================================================================\n")
    lines.append("#ifndef MODEL_DATA_H")
    lines.append("#define MODEL_DATA_H\n")
    lines.append("#include <cstdint>\n")

    lines.append(f"// 26 Acoustic Target Classes Map")
    lines.append("const char* const ACOUSTIC_CLASS_NAMES[] = {")
    for cls_name in classes:
        lines.append(f'    "{cls_name}",')
    lines.append("};\n")

    lines.append(f"const unsigned int ACOUSTIC_NUM_CLASSES = {len(classes)};\n")

    lines.append("alignas(8) const unsigned char g_model[] = {")

    # Format bytes into C++ hex arrays (12 bytes per line)
    byte_chunks = [f"0x{b:02x}" for b in hex_data]
    for i in range(0, len(byte_chunks), 12):
        chunk_str = ", ".join(byte_chunks[i:i+12])
        lines.append(f"    {chunk_str},")

    lines.append("};")
    lines.append(f"const unsigned int g_model_len = {len(hex_data)};\n")
    lines.append("#endif // MODEL_DATA_H\n")

    c_header_content = "\n".join(lines)
    os.makedirs(os.path.dirname(MODEL_H_FILE), exist_ok=True)
    with open(MODEL_H_FILE, 'w', encoding='utf-8') as f:
        f.write(c_header_content)

    print(f"  [OK] C++ Header written ({len(c_header_content)} bytes, {len(hex_data)} model bytes)")

def train_and_export():
    import tensorflow as tf
    from tensorflow import keras
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report, confusion_matrix

    print("="*70)
    print("TinyML 2D CNN MODEL TRAINER & INT8 C++ EXPORTER (SSD Accelerator)")
    print(f"TensorFlow Version: {tf.__version__}")
    print("="*70)

    X, y, classes = extract_features()

    # Split dataset: 80% Train, 10% Validation, 10% Test
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.50, random_state=42, stratify=y_temp)

    num_classes = len(classes)
    y_train_cat = keras.utils.to_categorical(y_train, num_classes)
    y_val_cat = keras.utils.to_categorical(y_val, num_classes)
    y_test_cat = keras.utils.to_categorical(y_test, num_classes)

    print(f"\nTrain set: {X_train.shape[0]} | Val set: {X_val.shape[0]} | Test set: {X_test.shape[0]}")

    # Build Depthwise-Separable 2D CNN (DS-CNN) tailored for MCU RAM/Flash limits
    input_shape = (X_train.shape[1], X_train.shape[2], 1)
    
    model = keras.Sequential([
        keras.layers.Input(shape=input_shape),

        # Conv Block 1
        keras.layers.Conv2D(16, (3, 3), padding='same', use_bias=False),
        keras.layers.BatchNormalization(),
        keras.layers.ReLU(),
        keras.layers.MaxPooling2D((2, 2)),

        # Depthwise Separable Block 1
        keras.layers.DepthwiseConv2D((3, 3), padding='same', use_bias=False),
        keras.layers.BatchNormalization(),
        keras.layers.ReLU(),
        keras.layers.Conv2D(32, (1, 1), padding='same', use_bias=False),
        keras.layers.BatchNormalization(),
        keras.layers.ReLU(),
        keras.layers.MaxPooling2D((2, 2)),

        # Depthwise Separable Block 2
        keras.layers.DepthwiseConv2D((3, 3), padding='same', use_bias=False),
        keras.layers.BatchNormalization(),
        keras.layers.ReLU(),
        keras.layers.Conv2D(64, (1, 1), padding='same', use_bias=False),
        keras.layers.BatchNormalization(),
        keras.layers.ReLU(),

        # Output Classifier
        keras.layers.GlobalAveragePooling2D(),
        keras.layers.Dropout(0.25),
        keras.layers.Dense(num_classes, activation='softmax')
    ])

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    print("\nModel Architecture Summary:")
    model.summary()

    callbacks = [
        keras.callbacks.EarlyStopping(monitor='val_accuracy', patience=6, restore_best_weights=True),
        keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3)
    ]

    print("\nTraining 2D CNN Model (25 Epochs)...")
    history = model.fit(
        X_train, y_train_cat,
        validation_data=(X_val, y_val_cat),
        epochs=25,
        batch_size=32,
        callbacks=callbacks
    )

    # Test set evaluation
    test_loss, test_acc = model.evaluate(X_test, y_test_cat, verbose=0)
    print(f"\n" + "="*50)
    print(f"FINAL TEST EVALUATION: Accuracy = {test_acc*100:.2f}% | Loss = {test_loss:.4f}")
    print("="*50)

    # Confusion matrix & Classification report
    y_pred = np.argmax(model.predict(X_test), axis=1)
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=classes))

    # TFLite INT8 Quantization
    print("\nQuantizing Model to INT8 TFLite...")
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]

    def representative_dataset():
        for i in range(min(100, len(X_train))):
            yield [np.expand_dims(X_train[i], axis=0)]

    converter.representative_dataset = representative_dataset
    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
    converter.inference_input_type = tf.int8
    converter.inference_output_type = tf.int8

    tflite_quant_model = converter.convert()

    # Save .tflite file
    with open(TFLITE_FILE, 'wb') as f:
        f.write(tflite_quant_model)
    print(f"Saved INT8 TFLite model: {TFLITE_FILE} ({len(tflite_quant_model)//1024} KB)")

    # Export C++ Header
    export_c_header(tflite_quant_model, classes)

    print("\n" + "="*70)
    print("TINYML MODEL TRAINING & C++ EXPORT COMPLETE!")
    print(f"C++ Model Header: E:\\software\\acoustic-surveillance\\firmware\\model_data.h")
    print(f"Test Accuracy: {test_acc*100:.2f}%")
    print("="*70)

if __name__ == '__main__':
    train_and_export()

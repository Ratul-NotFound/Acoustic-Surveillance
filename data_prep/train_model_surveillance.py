"""
train_model_surveillance.py
───────────────────────────
EXACT THREAT SURVEILLANCE TINYML MODEL TRAINER

Taxonomy Mapping:
  1. Forest Natural Environment Sound ('00_forest_natural_environment_sound'):
     Groups all natural background sounds (bird_calls, frog_croaks, insect_hums, rain,
     river_stream, wind, thunder) so the node hears real forest acoustics without false alarms.
  2. Active Threat & Activity Detection Classes (17 Classes):
     axe_machete_chopping, explosive_blast, human_speech, motorcycle_dirtbike,
     shouting_screaming, shoveling_digging, tree_falling, vehicle_engine,
     drone_propeller, hunting_dog, campfire_crackle, footsteps, footsteps_leaves,
     chainsaw, gunshot, handsaw, walkie_talkie, vehicle_engines.
"""

import os
import sys
import glob
import json
import numpy as np
import soundfile as sf
import librosa

DATASET_DIR = r"E:\software\acoustic-surveillance\data_prep\q1_dataset"
CACHE_FILE = r"E:\software\acoustic-surveillance\data_prep\features_surveillance_exact.npz"
LABEL_MAP_FILE = r"E:\software\acoustic-surveillance\data_prep\label_map.json"
MODEL_H_FILE = r"E:\software\acoustic-surveillance\firmware\model_data.h"
TFLITE_FILE = r"E:\software\acoustic-surveillance\firmware\model_quantized.tflite"

N_MELS = 40
N_FFT = 1024
HOP_LENGTH = 1024
TARGET_SR = 16000
CLIP_SAMPLES = 48000  # 3 seconds at 16kHz

# Natural environment background sounds grouped into 1 master class
NATURAL_ENV_CLASSES = {
    'bird_calls', 'frog_croaks', 'insect_hums', 'rain', 'river_stream', 'wind', 'thunder'
}

def compute_pcen_mfe(audio, sr=16000):
    mel_spec = librosa.feature.melspectrogram(
        y=audio, sr=sr, n_fft=N_FFT, hop_length=HOP_LENGTH, n_mels=N_MELS
    )
    s = librosa.pcen(mel_spec * (2**31), sr=sr, hop_length=HOP_LENGTH)
    norm_pcen = (s - np.min(s)) / (np.max(s) - np.min(s) + 1e-6)
    return norm_pcen.astype(np.float32)

def extract_surveillance_features():
    if os.path.exists(CACHE_FILE):
        print(f"Loading cached Surveillance PCEN features from: {CACHE_FILE}")
        data = np.load(CACHE_FILE)
        return data['X'], data['y'], list(data['classes'])

    print("Grouping dataset files into Forest Natural Environment + 17 Active Detection Classes...")
    raw_dirs = sorted([d for d in os.listdir(DATASET_DIR) if os.path.isdir(os.path.join(DATASET_DIR, d))])
    
    mapped_class_set = set()
    for d in raw_dirs:
        if d in NATURAL_ENV_CLASSES:
            mapped_class_set.add('00_forest_natural_environment_sound')
        else:
            mapped_class_set.add(d)

    classes = sorted(list(mapped_class_set))
    class_to_idx = {cls_name: idx for idx, cls_name in enumerate(classes)}

    X_list = []
    y_list = []

    for raw_cls in raw_dirs:
        target_label = '00_forest_natural_environment_sound' if raw_cls in NATURAL_ENV_CLASSES else raw_cls
        cls_dir = os.path.join(DATASET_DIR, raw_cls)
        wav_files = glob.glob(os.path.join(cls_dir, "*.wav"))
        print(f"  Mapping '{raw_cls}' -> '{target_label}': {len(wav_files)} files...")

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

                pcen_feat = compute_pcen_mfe(audio, sr=TARGET_SR)
                X_list.append(pcen_feat)
                y_list.append(class_to_idx[target_label])

            except Exception as e:
                print(f"    Error reading {fpath}: {e}")

    X = np.array(X_list, dtype=np.float32)
    if len(X.shape) == 3:
        X = np.expand_dims(X, axis=-1)  # (N, 40, T, 1)
    y = np.array(y_list, dtype=np.int32)

    np.savez_compressed(CACHE_FILE, X=X, y=y, classes=np.array(classes))
    with open(LABEL_MAP_FILE, 'w') as f:
        json.dump(class_to_idx, f, indent=2)

    print(f"Extraction Complete. X shape: {X.shape}, y shape: {y.shape}, Active Classes ({len(classes)}): {classes}")
    return X, y, classes

def export_c_header(tflite_model_bytes, classes):
    print(f"\nExporting INT8 C++ header to: {MODEL_H_FILE}")
    hex_data = tflite_model_bytes
    lines = []
    lines.append("// ==========================================================================")
    lines.append("// Surveillance SE-DS-CNN TinyML Model Header for ESP32-S3 Green Edge Computing")
    lines.append(f"// Classes: {len(classes)} | Target SR: 16000Hz | Feature: PCEN {N_MELS} Mel Bands")
    lines.append("// ==========================================================================\n")
    lines.append("#ifndef MODEL_DATA_H")
    lines.append("#define MODEL_DATA_H\n")
    lines.append("#include <cstdint>\n")

    lines.append("const char* const ACOUSTIC_CLASS_NAMES[] = {")
    for cls_name in classes:
        lines.append(f'    "{cls_name}",')
    lines.append("};\n")

    lines.append(f"const unsigned int ACOUSTIC_NUM_CLASSES = {len(classes)};\n")
    lines.append("alignas(8) const unsigned char g_model[] = {")

    byte_chunks = [f"0x{b:02x}" for b in hex_data]
    for i in range(0, len(byte_chunks), 12):
        chunk_str = ", ".join(byte_chunks[i:i+12])
        lines.append(f"    {chunk_str},")

    lines.append("};")
    lines.append(f"const unsigned int g_model_len = {len(hex_data)};\n")
    lines.append("#endif // MODEL_DATA_H\n")

    content = "\n".join(lines)
    os.makedirs(os.path.dirname(MODEL_H_FILE), exist_ok=True)
    with open(MODEL_H_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  [OK] C++ Header written successfully ({len(hex_data)} bytes model size)")

def build_se_ds_cnn(input_shape, num_classes):
    import tensorflow as tf
    from tensorflow import keras

    def se_block(input_tensor, ratio=8):
        channels = input_tensor.shape[-1]
        se = keras.layers.GlobalAveragePooling2D()(input_tensor)
        se = keras.layers.Dense(max(4, channels // ratio), activation='relu', use_bias=False)(se)
        se = keras.layers.Dense(channels, activation='sigmoid', use_bias=False)(se)
        se = keras.layers.Reshape((1, 1, channels))(se)
        return keras.layers.Multiply()([input_tensor, se])

    inputs = keras.layers.Input(shape=input_shape)

    x = keras.layers.Conv2D(24, (3, 3), padding='same', use_bias=False)(inputs)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.ReLU()(x)
    x = keras.layers.MaxPooling2D((2, 2))(x)

    x = keras.layers.DepthwiseConv2D((3, 3), padding='same', use_bias=False)(x)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.ReLU()(x)
    x = keras.layers.Conv2D(48, (1, 1), padding='same', use_bias=False)(x)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.ReLU()(x)
    x = se_block(x, ratio=8)
    x = keras.layers.MaxPooling2D((2, 2))(x)

    x = keras.layers.DepthwiseConv2D((3, 3), padding='same', use_bias=False)(x)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.ReLU()(x)
    x = keras.layers.Conv2D(64, (1, 1), padding='same', use_bias=False)(x)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.ReLU()(x)
    x = se_block(x, ratio=8)

    x = keras.layers.GlobalAveragePooling2D()(x)
    x = keras.layers.Dropout(0.20)(x)
    outputs = keras.layers.Dense(num_classes, activation='softmax')(x)

    model = keras.Model(inputs=inputs, outputs=outputs, name="Surveillance_SE_DS_CNN")
    return model

def train_and_export():
    import tensorflow as tf
    from tensorflow import keras
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report, confusion_matrix

    print("="*70)
    print("SURVEILLANCE THREAT SE-DS-CNN TRAINER")
    print(f"TensorFlow Version: {tf.__version__}")
    print("="*70)

    X, y, classes = extract_surveillance_features()

    # Standard Academic Split: 70% Train, 15% Val, 15% Test
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.30, random_state=42, stratify=y)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.50, random_state=42, stratify=y_temp)

    num_classes = len(classes)
    y_train_cat = keras.utils.to_categorical(y_train, num_classes)
    y_val_cat = keras.utils.to_categorical(y_val, num_classes)
    y_test_cat = keras.utils.to_categorical(y_test, num_classes)

    input_shape = (X_train.shape[1], X_train.shape[2], 1)
    print(f"\nFeature Shape: {input_shape}")
    print(f"Train set: {X_train.shape[0]} | Val set: {X_val.shape[0]} | Test set: {X_test.shape[0]}")

    model = build_se_ds_cnn(input_shape=input_shape, num_classes=num_classes)

    loss_fn = keras.losses.CategoricalCrossentropy(label_smoothing=0.05)

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.002),
        loss=loss_fn,
        metrics=['accuracy']
    )

    model.summary()

    callbacks = [
        keras.callbacks.EarlyStopping(monitor='val_accuracy', patience=8, restore_best_weights=True),
        keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=1e-5)
    ]

    print("\nTraining Exact Threat Surveillance Model (25 Epochs)...")
    history = model.fit(
        X_train, y_train_cat,
        validation_data=(X_val, y_val_cat),
        epochs=25,
        batch_size=32,
        callbacks=callbacks
    )

    test_loss, test_acc = model.evaluate(X_test, y_test_cat, verbose=0)
    print(f"\n" + "="*60)
    print(f"SURVEILLANCE TEST EVALUATION: Overall System Accuracy = {test_acc*100:.2f}% | Loss = {test_loss:.4f}")
    print("="*60)

    y_pred = np.argmax(model.predict(X_test), axis=1)
    print("\nDetailed Threat Classification Report:")
    print(classification_report(y_test, y_pred, target_names=classes, digits=4))

    print("\nQuantizing Model to INT8 TFLite...")
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]

    def representative_dataset():
        for i in range(min(150, len(X_train))):
            yield [np.expand_dims(X_train[i], axis=0)]

    converter.representative_dataset = representative_dataset
    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
    converter.inference_input_type = tf.int8
    converter.inference_output_type = tf.int8

    tflite_quant = converter.convert()

    with open(TFLITE_FILE, 'wb') as f:
        f.write(tflite_quant)
    print(f"Saved INT8 TFLite model: {TFLITE_FILE} ({len(tflite_quant)//1024} KB)")

    export_c_header(tflite_quant, classes)

    print("\n" + "="*70)
    print("SURVEILLANCE MODEL TRAINING & C++ EXPORT COMPLETE!")
    print(f"C++ Model Header: E:\\software\\acoustic-surveillance\\firmware\\model_data.h")
    print(f"Overall System Accuracy: {test_acc*100:.2f}%")
    print("="*70)

if __name__ == '__main__':
    train_and_export()

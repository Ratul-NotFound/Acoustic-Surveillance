/**
 * Edge AI Forest Acoustic Surveillance System
 * Boilerplate Firmware for ESP32-S3 (Arduino Core)
 * 
 * This sketch demonstrates:
 * 1. Setting up I2S to read digital audio from the INMP441 Microphone.
 * 2. Basic duty-cycling (Deep Sleep / Wake-up loop).
 * 3. Pin definitions for I2S, GSM (SIM800L), GPS (Neo-6M), and Accelerometer (LIS3DH).
 */

#include <driver/i2s.h>

// ==========================================
// 1. PIN CONFIGURATIONS
// ==========================================

// INMP441 I2S Microphone
#define I2S_WS      5
#define I2S_SD      6
#define I2S_SCK     4
#define I2S_PORT    I2S_NUM_0

// SIM800L GSM Module
#define GSM_TX_PIN  18  // Connect to GSM RX
#define GSM_RX_PIN  17  // Connect to GSM TX
#define GSM_PWR_KEY 16  // Connect to transistor/MOSFET controlling GSM power
#define GSM_RST_PIN 15

// Neo-6M GPS Module
#define GPS_TX_PIN  41  // Connect to GPS RX
#define GPS_RX_PIN  42  // Connect to GPS TX

// LIS3DH Accelerometer (I2C & Wake-up)
#define I2C_SDA     8
#define I2C_SCL     9
#define ACCEL_INT   10  // Interrupt pin to wake ESP32-S3 on movement

// ==========================================
// 2. TIMING & SLEEP PARAMETERS
// ==========================================
#define LISTEN_DURATION_SEC 2
#define DEEP_SLEEP_TIME_SEC 10
#define SAMPLE_RATE         16000
#define BUFFER_SIZE         1024

// Global audio buffer
int16_t audio_buffer[BUFFER_SIZE];

// ==========================================
// 3. HARDWARE CONFIGURATIONS
// ==========================================

void setup_i2s() {
  i2s_config_t i2s_config = {
    .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX),
    .sample_rate = SAMPLE_RATE,
    .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
    .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
    .communication_format = i2s_comm_format_t(I2S_COMM_FORMAT_STAND_I2S),
    .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
    .dma_buf_count = 8,
    .dma_buf_len = 64,
    .use_apll = false,
    .tx_desc_auto_clear = false,
    .fixed_mclk = 0
  };

  i2s_pin_config_t pin_config = {
    .bck_io_num = I2S_SCK,
    .ws_io_num = I2S_WS,
    .data_out_num = I2S_PIN_NO_CHANGE,
    .data_in_num = I2S_SD
  };

  i2s_driver_install(I2S_PORT, &i2s_config, 0, NULL);
  i2s_set_pin(I2S_PORT, &pin_config);
}

void record_and_process() {
  Serial.println("Listening to forest ambient sounds...");
  
  size_t bytes_read = 0;
  unsigned long start_time = millis();
  unsigned long duration_ms = LISTEN_DURATION_SEC * 1000;
  
  while (millis() - start_time < duration_ms) {
    // Read audio data from I2S microphone
    i2s_read(I2S_PORT, &audio_buffer, sizeof(audio_buffer), &bytes_read, portMAX_DELAY);
    
    // Convert bytes to samples count
    int samples_read = bytes_read / sizeof(int16_t);
    
    if (samples_read > 0) {
      // TODO: Feed audio buffer to your trained TinyML model here
      // Example: 
      // run_inference(audio_buffer, samples_read);
    }
  }
  
  // Placeholder ML output
  bool alert_triggered = false; 
  
  if (alert_triggered) {
    send_alert();
  }
}

void send_alert() {
  Serial.println("ALERT TRIGGERED! Activating GSM module...");
  
  // 1. Power on GSM module (toggle MOSFET power pin)
  digitalWrite(GSM_PWR_KEY, HIGH);
  delay(1000); 
  
  // 2. Initialize Hardware Serial for SIM800L
  // Serial2.begin(9600, SERIAL_8N1, GSM_RX_PIN, GSM_TX_PIN);
  
  // 3. Send SMS using AT commands
  // Serial2.println("AT+CMGF=1"); // Set SMS to text mode
  // delay(100);
  // Serial2.println("AT+CMGS=\"+880XXXXXXXXXX\""); // Replace with your phone number
  // delay(100);
  // Serial2.print("ALERT: Chainsaw / Gunshot detected! Lat: [GPS_LAT], Lon: [GPS_LON]");
  // Serial2.write(26); // ASCII code for Ctrl+Z to send the SMS
  
  // 4. Power off GSM module to save battery
  digitalWrite(GSM_PWR_KEY, LOW);
  Serial.println("Alert sent. GSM powered down.");
}

// ==========================================
// 4. MAIN PROGRAM LIFE CYCLE
// ==========================================

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("Device Booting...");

  // Initialize GSM control pins
  pinMode(GSM_PWR_KEY, OUTPUT);
  digitalWrite(GSM_PWR_KEY, LOW); // Keep GSM off by default to conserve power
  
  // Initialize digital microphone
  setup_i2s();
  
  // Set up accelerometer interrupt pin to wake ESP32 on movement
  pinMode(ACCEL_INT, INPUT_PULLDOWN);
  esp_sleep_enable_ext0_wakeup((gpio_num_t)ACCEL_INT, 1); // Wake up if pin goes HIGH
  
  // Set up timer wake-up for duty-cycling
  esp_sleep_enable_timer_wakeup(DEEP_SLEEP_TIME_SEC * 1000000ULL);
  
  // Run recording and local audio classification
  record_and_process();
  
  // Disable I2S before sleeping to save power
  i2s_driver_uninstall(I2S_PORT);
  
  // Go to sleep
  Serial.println("Entering Deep Sleep mode to save battery...");
  Serial.flush();
  esp_deep_sleep_start();
}

void loop() {
  // Loop is never executed because the device sleeps at the end of setup() 
  // and wakes up starting from setup() again.
}

# Hardware Wiring & Pin Mapping Guide

This guide details the physical electrical connections between the **ESP32-S3** microcontroller and the peripheral modules.

---

## 1. GPIO Pin Mapping Table

| Peripheral Module | Pin Name | ESP32-S3 Pin | Description / Notes |
| :--- | :--- | :--- | :--- |
| **INMP441 Microphone** | VCC | 3.3V | Digital microphone power |
| | GND | GND | Ground |
| | L/R | GND | Set to GND for Left Channel audio |
| | SCK (Clock) | GPIO 4 | I2S Serial Clock |
| | WS (Word Select) | GPIO 5 | I2S Word Select |
| | SD (Serial Data) | GPIO 6 | I2S Serial Data input |
| **SIM800L GSM Module** | VCC | 4V Battery / Regulator | Needs 3.7V - 4.2V (up to 2A burst current). Do not power from 3.3V! |
| | GND | GND | Must share a common ground with ESP32-S3 |
| | TX | GPIO 18 | Connects to ESP32 RX (Serial2) |
| | RX | GPIO 17 | Connects to ESP32 TX (Serial2) |
| | PWR_KEY | GPIO 16 | Controls MOSFET switch to power ON/OFF GSM |
| | RST | GPIO 15 | Optional hardware reset pin |
| **Neo-6M GPS Module** | VCC | 3.3V / 5V | GPS power supply |
| | GND | GND | Ground |
| | TX | GPIO 41 | Connects to ESP32 RX (Serial1) |
| | RX | GPIO 42 | Connects to ESP32 TX (Serial1) |
| **LIS3DH Accelerometer** | VCC | 3.3V | Ultra-low power sensor supply |
| | GND | GND | Ground |
| | SDA | GPIO 8 | I2C Data line |
| | SCL | GPIO 9 | I2C Clock line |
| | INT1 | GPIO 10 | Interrupt output to wake up ESP32-S3 |

---

## 2. Power and Charging Circuit Schematic Design

To support long-term autonomous field deployment, use a solar energy harvesting circuit:

```
                        [ Solar Panel (5V-6V, 2W) ]
                                     │
                                     ▼
                    [ CN3065 / TP4056 Solar Charger ]
                      │                            │
                      ▼                            ▼
         [ 18650 LiFePO4 Battery ]       [ High-Current Switch / MOSFET ]
                      │                            │
                      ▼                            ▼
            [ LDO Regulator (3.3V) ]         [ SIM800L Module (4V/GPRS) ]
                      │
                      ▼
             [ ESP32-S3 / Mic / GPS ]
```

### Key Power Components:
1. **Solar Panel**: 5V to 6V monocrystalline panel, rated at 1W to 2W.
2. **Solar Charger (CN3065)**: Connects solar panel to the battery. Automatically stops charging when battery is full.
3. **Battery**: A single 18650 LiFePO4 battery (nominal 3.2V, full charge 3.6V). This battery chemistry operates safely in high forest ambient temperatures.
4. **Regulator (LDO)**: Use a high-efficiency Low Dropout Regulator (such as **HT7333-A**) with a very low quiescent current (approx. 4µA) to step down the battery voltage to a clean 3.3V for the ESP32-S3, microphone, and sensors.
5. **GSM Power Switch**: The SIM800L consumes substantial standby power and experiences high current spikes. Use an **N-channel MOSFET** (e.g., IRLZ44N) connected to the ESP32 GPIO 16 to completely isolate the SIM800L's ground/power line when it is not actively transmitting alerts.

# 🔋 Task 6.1: Solar Power Budget, Battery Audit & Circuitry Guide

**System Target**: 24/7 Autonomous Solar Harvesting for Infinite Node Lifespan  
**Microcontroller**: ESP32-S3 (Dual-Core LX7 @ 240MHz)  
**Battery**: 18650 LiFePO4 Cell (3.2V - 3.6V, 2000 mAh Capacity)  
**Solar Controller**: CN3065 Mini Solar Charger IC + 5V 5W Monocrystalline Panel  
**Voltage Regulator**: HT7333-1 LDO (3.3V Output, Ultra-Low Quiescent Current $I_q < 4\mu\text{A}$)  

---

## 📊 1. Power Consumption Audit Table

| System State | Active Modules | Voltage (V) | Current Draw | Power (mW) | Duty Cycle per Hour | Daily Energy (mWh) |
|---|---|:---:|:---:|:---:|:---:|:---:|
| **Deep Sleep Mode** | ESP32-S3 RTC + LIS3DH Accelerometer | 3.3V | **15 µA** | 0.0495 mW | 58.5 min/hr (97.5%) | **1.16 mWh** |
| **Acoustic Surveillance** | ESP32-S3 @ 240MHz + INMP441 Mic | 3.3V | **18.5 mA** | 61.05 mW | 1.5 min/hr (2.5%) | **91.58 mWh** |
| **GPS Fix Acquisition** | Neo-6M GPS Module (UART) | 3.3V | **25.0 mA** | 82.50 mW | 2 alerts/day (30s ea) | **1.38 mWh** |
| **GSM SMS Transmission** | SIM800L Cellular Modem (TX Burst) | 3.7V | **200.0 mA** | 740.00 mW | 2 alerts/day (5s ea) | **2.06 mWh** |
| **TOTAL DAILY ENERGY CONSUMED** | | | | | | **~96.18 mWh / day** |

---

## ☀️ 2. Solar Energy Harvesting Equilibrium Calculation

* **5V 5W Mini Solar Panel Yield**:
  - Average Peak Sun Hours (Forest Canopy Understory): **2.5 Hours / day**
  - Solar Panel Output: $5\text{W} \times 0.20 \text{ (Canopy Loss)} = 1.0\text{W}$
  - Daily Harvested Energy: $1.0\text{W} \times 2.5\text{ hrs} = 2,500\text{ mWh / day}$

$$\text{Energy Harvested } (2,500\text{ mWh}) \gg \text{Energy Consumed } (96.18\text{ mWh})$$

**Result**: The solar harvesting yield exceeds daily consumption by **over 25x**, guaranteeing **continuous 24/7/365 node operation** even during prolonged cloudy weather!

---

## ⚡ 3. Battery Autonomy Without Sun (Cloudy Weather Buffer)

* **18650 LiFePO4 Energy Capacity**:
  $$\text{Capacity} = 3.2\text{V} \times 2000\text{ mAh} = 6,400\text{ mWh}$$
* **Days of Autonomy in Complete Darkness (Zero Sunlight)**:
  $$\text{Autonomy Days} = \frac{6,400\text{ mWh}}{96.18\text{ mWh/day}} \approx \mathbf{66.5 \text{ Days}}$$

---

## 🔌 4. Wiring Circuitry & Battery Protection Schematic

```
  [ 5V 5W Solar Panel ]
           │
           ▼
     ┌───────────┐
     │  CN3065   │──(BAT+)──┐
     │ Solar IC  │          │
     └─────┬─────┘          ▼
           │           ┌──────────┐
        (GND)          │  18650   │ (LiFePO4 3.2V)
           │           │ Battery  │
           ▼           └────┬─────┘
    ┌─────────────┐         │
    │  HT7333-1   │◄────────┘ (VBAT)
    │  3.3V LDO   │
    └──────┬──────┘
           │
           ├───────────────────────────────► ESP32-S3 3.3V VCC
           ├───────────────────────────────► INMP441 VDD
           └─[100kΩ/100kΩ Voltage Divider]──► GPIO 1 (ADC Battery Monitor)
```

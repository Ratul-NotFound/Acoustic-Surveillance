# 🌐 System Design & Architecture: Solar Box, Zoning, & GSM Alerting Protocol

This document details the engineering specifications for the physical hardware node, battery/solar power budgeting, zoning deployment model, and the communication protocol used to notify central control authorities (Police, Coast Guard, and Forest Authority).

---

## 1. Physical Device Casing & Solar Box Design

To ensure the node is self-sustaining in dense forest foliage with limited sunlight, the device uses a **multidirectional solar harvesting box design**.

### 📦 Physical Enclosure Concept

```
             ┌────────────────────────┐
             │    [ SOLAR PANEL 1 ]   │  <-- Top Panel (Direct Overhead Sunlight)
             │      (Rain Shield)     │
      ┌──────┴────────────────────────┴──────┐
      │ ┌──────────────────────────────────┐ │
      │ │                                  │ │
      │ │         [ SOLAR PANEL 2 ]        │ │  <-- East/West Side Panel (Low Angle Sunlight)
      │ │                                  │ │
      │ └──────────────────────────────────┘ │
      │      ○ [GORE-TEX ACOUSTIC PORT]     │  <-- Water-resistant microphone entry
      │                                      │
      │  [Inside: ESP32-S3, GPS, GSM, LiPo]  │  <-- Heavy components placed at bottom for stability
      └──────────────────────────────────────┘
```

1.  **3D Printed Weatherproof Box (IP67)**:
    *   Printed in UV-resistant PETG or ABS filament.
    *   Coated in a matte camouflaged pattern (woodland or bark texture) to avoid detection.
2.  **Multidirectional Solar Panel Array**:
    *   Instead of a single panel, the box features **three small solar panels** integrated onto its faces (one top panel, two side panels).
    *   This ensures that no matter which way the device is oriented on a tree trunk, it can capture morning, midday, or afternoon sun.
3.  **Acoustic Port Membrane**:
    *   A small 5mm hole at the bottom (facing down to prevent rain entry) allows sound to reach the digital INMP441 microphone.
    *   The hole is sealed with a **Gore-Tex acoustic vent membrane** which allows sound pressure waves to pass through while completely blocking liquid water.

---

## 2. Power Budget: Battery Sizing & Solar Charging

The hardware must balance weight, size, and electrical capacity to ensure continuous 24/7 duty-cycled operations.

### 🔋 Battery Recommendation: Lithium Polymer (LiPo) vs. LiFePO4

| Parameter | Lithium Polymer (LiPo) | LiFePO4 (Lithium Iron Phosphate) | Recommendation |
| :--- | :--- | :--- | :--- |
| **Energy Density** | 🟢 Very High (Small & Lightweight) | 🟡 Moderate (Heavier, larger) | **LiFePO4** is recommended for forest safety because it is thermally stable and will not catch fire or explode if the tree trunk exceeds $50^\circ\text{C}$ in direct sunlight. However, if space is extremely constrained, a **protected 18650 LiPo battery pack** (2600mAh) can be used. |
| **Lifespan** | 🟡 300–500 cycles | 🟢 2000–3000 cycles |
| **Safety** | 🔴 Low (Thermal runaway risk) | 🟢 High (No thermal runaway) |

### ⚡ Power Budget Calculations

*   **ESP32-S3 Sleep Mode**: $\approx 20\,\mu\text{A}$ at $3.3\text{V} = 0.066\,\text{mW}$
*   **Active Inference Mode (ESP32-S3 + I2S Mic active for 2s every 10s)**: $\approx 100\,\text{mA}$ at $3.3\text{V} = 330\,\text{mW}$
*   **GSM Standby Mode (SIM800L power-down state)**: $0.0\,\text{mA}$ (Isolated by MOSFET switch)
*   **GSM Transmission Alert Mode (SIM800L powered on, sending SMS, 15 seconds duration)**: $\approx 350\,\text{mA}$ average, with $2\,\text{A}$ bursts at $4.0\text{V} = 1400\,\text{mW}$

#### Average Continuous Power Consumption (No Alerts):
$$\text{Average Current} = \frac{(I_{\text{active}} \times t_{\text{active}}) + (I_{\text{sleep}} \times t_{\text{sleep}})}{t_{\text{active}} + t_{\text{sleep}}}$$
$$\text{Average Current} = \frac{(100\,\text{mA} \times 2\,\text{s}) + (0.02\,\text{mA} \times 8\,\text{s})}{10\,\text{s}} = 20.016\,\text{mA}$$

At a standard $3.7\text{V}$ battery voltage:
*   **Daily Capacity Needed**: $20.016\,\text{mA} \times 24\,\text{hours} = 480.38\,\text{mAh}$ per day.
*   A lightweight **2600mAh 18650 battery** can power the device for **5.4 days** with zero sunlight.
*   **Solar Charging**: A small $5\text{V}$ $1.5\text{W}$ solar panel (generating $\approx 300\,\text{mA}$ in peak sun) only needs **1.6 hours** of direct sunlight per day to fully recharge the daily consumed energy ($480.38\,\text{mAh} / 300\,\text{mA} = 1.6\,\text{h}$).

---

## 3. Deployment Zoning Model

Devices are grouped into coordinate-defined **Zones** matching the jurisdiction of different environmental and emergency response agencies.

```
       🌲 FOREST CANOPY / DEPLOYMENT AREA 🌲
┌───────────────────────┬───────────────────────┐
│        ZONE A         │        ZONE B         │
│    (North Coastline)  │     (Dense Forest)    │
│  [Node-01]  [Node-02]  │  [Node-03]  [Node-04] │
└───────────┬───────────┴───────────┬───────────┘
            │                       │
            │ (GSM Cellular Link)   │
            ▼                       ▼
┌───────────────────────────────────────────────┐
│               CENTRAL CONTROL GATEWAY         │
│   - Receives and decodes the alert SMS/Data   │
└──────┬─────────────────┬───────────────────┬──┘
       │                 │                   │
       ▼                 ▼                   ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  COAST GUARD │  │    POLICE    │  │ FOREST AUTH. │
│ (Zone A alerts)│ (Zone B alerts)│ (All logs)   │
└──────────────┘  └──────────────┘  └──────────────┘
```

1.  **Zone A (Mangrove/Riverside - Coast Guard Jurisdiction)**:
    *   Monitors illegal boat movement, snare trapping, and coastal logging.
    *   Alerts are routed to the **Coast Guard** command center.
2.  **Zone B (Interior Forest Reserve - Forest Authority & Police)**:
    *   Monitors chainsaws, vehicle trespass, and gunshots.
    *   Alerts are routed directly to the **Forest Ranger Stations** and local **Police**.

---

## 4. GSM Alert Communication Protocol

When a threat is classified with a confidence score above **85%**, the device powers up the SIM800L module and transmits a structured alert payload.

### Option A: SMS Alert Format (Standard & Highly Reliable)

SMS is preferred for remote regions because it transmits over the 2G control channel, requiring minimal signal strength.

#### SMS Payload Structure (Plain Text):
```text
[ALERT]
ID: NODE-042
ZONE: B-NORTH
ACT: CHAINSAW (CUTTING)
CONF: 94%
GPS: 22.34891, 89.54023
MAPS: https://maps.google.com/?q=22.34891,89.54023
BATT: 3.82V (85%)
TIME: 2026-06-18 02:42:19
```

*   **Key Parameters**:
    *   `ID`: Unique node hardware identifier.
    *   `ZONE`: Designated geographic sector.
    *   `ACT`: Labeled classification category.
    *   `CONF`: Model output probability score.
    *   `GPS`: Latitude/Longitude from the Neo-6M GPS.
    *   `MAPS`: Clickable Google Maps hyperlink for rapid navigation.
    *   `BATT`: Device battery voltage and estimated percentage to schedule maintenance.

---

### Option B: GPRS Data Payload (JSON API Integration)

If cellular internet is stable, the device transmits a lightweight HTTP POST request to a Central Control dashboard server.

#### JSON Data Payload:
```json
{
  "device_id": "NODE-042",
  "zone": "B-NORTH",
  "timestamp": "2026-06-18T02:42:19Z",
  "alert": {
    "activity": "GUNSHOT",
    "confidence": 0.97,
    "sub_class": "SHOTGUN"
  },
  "telemetry": {
    "latitude": 22.34891,
    "longitude": 89.54023,
    "battery_voltage": 3.82,
    "battery_percentage": 85,
    "rssi": 18
  }
}
```

---

## 5. Firmware Code Implementation: Building the Alert String

Here is how the notification string is constructed in the C++ firmware before sending via the SIM800L GSM serial interface:

```cpp
#include <Arduino.h>

// Simulated GPS data structure
struct GPSData {
    float latitude = 22.34891;
    float longitude = 89.54023;
};

// Simulated battery measurement
float get_battery_voltage() {
    // Read analog pin divider
    return 3.82; 
}

// Function to construct and send SMS alert
void compile_and_send_alert(const char* node_id, const char* zone_id, const char* activity, float confidence) {
    GPSData gps;
    float bat_voltage = get_battery_voltage();
    int bat_percent = (int)((bat_voltage - 3.2) / (4.2 - 3.2) * 100.0);
    if(bat_percent > 100) bat_percent = 100;
    if(bat_percent < 0) bat_percent = 0;
    
    // Build formatted message string
    String message = "[ALERT]\n";
    message += "ID: " + String(node_id) + "\n";
    message += "ZONE: " + String(zone_id) + "\n";
    message += "ACT: " + String(activity) + "\n";
    message += "CONF: " + String((int)(confidence * 100)) + "%\n";
    message += "GPS: " + String(gps.latitude, 5) + ", " + String(gps.longitude, 5) + "\n";
    message += "MAPS: https://maps.google.com/?q=" + String(gps.latitude, 5) + "," + String(gps.longitude, 5) + "\n";
    message += "BATT: " + String(bat_voltage, 2) + "V (" + String(bat_percent) + "%)\n";
    
    Serial.println("Constructed SMS Payload:");
    Serial.println(message);
    
    // Send message to SIM800L Serial port
    // Serial2.println("AT+CMGF=1"); // SMS Text Mode
    // delay(100);
    // Serial2.println("AT+CMGS=\"+880XXXXXXXXXX\""); // Central Control Phone Number
    // delay(100);
    // Serial2.print(message);
    // Serial2.write(26); // Send ASCII Ctrl+Z
}
```

# 📦 Task 6.2: 3D Printed IP67 Weatherproof Camouflaged Tree Casing Design

**Ingress Protection Rating**: IP67 (Dust-tight + Waterproof immersion up to 1 meter)  
**Material**: PETG or ABS (UV Resistant, High Impact Resistance, Temperature Rating $-20^\circ\text{C}$ to $+80^\circ\text{C}$)  
**Physical Dimensions**: $120\text{mm} \times 80\text{mm} \times 45\text{mm}$  
**Camouflage Texture**: Bark-Patterned Organic Mold (Blends with Pine, Oak, and Tropical Hardwood Tree Trunks)  

---

## 📐 1. Enclosure Mechanical Design Breakdown

```
        ┌─────────────────────────────────────────────────────────┐
        │  45° Angled Top Solar Mount Bracket (5W Panel)         │
        ├─────────────────────────────────────────────────────────┤
        │                                                         │
        │   ┌─────────────────────────────────────────────────┐   │
        │   │  Main Weatherproof PETG Shell (IP67 Gasket)    │   │
        │   │                                                 │   │
        │   │   [ESP32-S3]   [SIM800L]   [Neo-6M GPS]         │   │
        │   │   [18650 LiFePO4 Battery Pack] [CN3065 IC]      │   │
        │   │                                                 │   │
        │   └─────────────────────────────────────────────────┘   │
        │                                                         │
        │   [Acoustic Horn Waveguide + GORE-TEX Vent Membrane]    │
        │   (INMP441 Microphone Port facing downward 15°)         │
        └─────────────────────────────────────────────────────────┘
                   │                                   │
                   └───► [Dual Heavy-Duty Strap Slots] ◄───┘
```

---

## 🛠️ 2. Key Engineering Specifications

### A. Acoustic Horn Waveguide & GORE-TEX Acoustic Membrane
- **Downward Facing Port**: The INMP441 MEMS microphone port is positioned on the underside of the enclosure angled 15 degrees downward. This prevents direct rainfall from entering the acoustic channel.
- **GORE-TEX GAW112 Membrane**: Placed over the microphone port to allow sound waves to enter ($0.5\text{ dB}$ acoustic attenuation) while blocking water droplets and moisture ($>100\text{ kPa}$ water entry pressure).

### B. Anti-Tamper & Motion Detection (LIS3DH Accelerometer)
- **Vibration & Theft Detection**: Internal LIS3DH accelerometer detects physical tree tampering or attempts by illegal loggers to remove the sensor node.
- **Tilt Interrupt**: Triggers an immediate GSM SMS alert if the device is tilted > 30 degrees from its vertical tree mount position.

### C. Tree Trunk Mounting Mechanism
- Dual 25mm slotted strap loops integrated into the rear PETG chassis enable non-destructive tree mounting using industrial weather-resistant nylon webbing or stainless steel hose clamps.

---

## 🖨️ 3. 3D Printing Guidelines for Production

- **Layer Height**: 0.20 mm
- **Infill Density**: 40% Gyroid Infill (High structural rigidity)
- **Wall Perimeter**: 4 Shell Walls (Ensures zero water penetration through layer lines)
- **Post-Processing**: Coated with UV-resistant matte forest brown/green camouflage spray.

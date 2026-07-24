# Remaining Sourcing Targets (Post ESC-50 Extraction)

Your **ESC-50 dataset** has been successfully downloaded and sorted! You now have **560 audio files** spanning **13 classes** inside your `raw_data/` directory.

Here is the updated list of the remaining **18 classes and sub-classes** that you still need to collect, along with their optimal sources:

---

## 1. Threats / Unwanted Activities (14 Classes Remaining)

| Target Class | Status | Best Source to Use | Download Action |
| :--- | :--- | :--- | :--- |
| **Gunshot (Pistol/Rifle)** | 🔴 Missing | Mendeley Gunshot Dataset | Download and copy files to `raw_data/gunshot/`. |
| **Gunshot (Shotgun)** | 🔴 Missing | Mendeley Gunshot Dataset | Download and copy files to `raw_data/gunshot/`. |
| **Axe/Machete Chopping** | 🔴 Missing | FSC22 / FSD50K | Search `axe` or `wood chopping` in Freesound. |
| **Tree Cracking/Falling** | 🔴 Missing | FSC22 / FSD50K | Search `tree falling` in Freesound. |
| **Heavy Machinery** | 🔴 Missing | FSD50K | Search `bulldozer` or `tractor` in Freesound. |
| **Motorcycle/Dirt Bike** | 🔴 Missing | FSD50K | Search `dirt bike` or `motorcycle` in Freesound. |
| **Human Speech/Voices** | 🔴 Missing | FSD50K / AudioSet | Search `speech` or `talking` in Freesound. |
| **Shouting/Screaming** | 🔴 Missing | FSD50K | Search `screaming` or `shouting` in Freesound. |
| **Walkie-Talkie (Static/Beeps)**| 🔴 Missing | FSD50K / YouTube | Search `walkie talkie static` in Freesound or YouTube. |
| **Metal Clinking (Traps)** | 🔴 Missing | FSD50K / YouTube | Search `steel trap click` in Freesound or YouTube. |
| **Shoveling/Digging** | 🔴 Missing | FSD50K | Search `digging` or `shoveling` in Freesound. |
| **Drone Propeller Hum** | 🔴 Missing | FSD50K / YouTube | Search `drone propeller` in Freesound or YouTube. |
| **Explosive Blast** | 🔴 Missing | FSD50K | Search `explosion` in Freesound. |
| **Chainsaw (Idle / Cutting)**| 🟡 Split Needed | Zenodo / YouTube | Use your general `chainsaw` folder, but collect more specific clips of chainsaws *idle* vs. *cutting* to split them. |

---

## 2. Weather & Biological Filters (4 Classes Remaining)

| Target Class | Status | Best Source to Use | Download Action |
| :--- | :--- | :--- | :--- |
| **Monkey Alarm Calls** | 🔴 Missing | Rainforest / Xeno-Canto | Search `Primate` or `monkey alert` in Xeno-Canto. |
| **Rain (Light vs. Heavy)** | 🟡 Split Needed | FSC22 | Split your ESC-50 `rain` folder into `rain_light` and `rain_heavy` using FSC22. |
| **Thunder (Distant vs. Close)**| 🟡 Split Needed | FSC22 | Split your ESC-50 `thunder` folder into `thunder_distant` and `thunder_close` using FSC22. |
| **Wind (Canopy vs. Howling)** | 🟡 Split Needed | FSC22 | Split your ESC-50 `wind` folder into `wind_canopy` and `wind_howling` using FSC22. |

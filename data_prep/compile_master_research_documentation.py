"""
compile_master_research_documentation.py
──────────────────────────────────────────
Compiles ALL project documentation files into ONE SINGLE, EXTREMELY DETAILED,
STEP-BY-STEP MASTER RESEARCH DOCUMENTATION FILE.

Outputs:
  - E:\\software\\acoustic-surveillance\\manuscripts\\COMPLETE_RESEARCH_MASTER_DOCUMENTATION.md
  - E:\\software\\acoustic-surveillance\\manuscripts\\COMPLETE_RESEARCH_MASTER_DOCUMENTATION.doc
  - E:\\software\\acoustic-surveillance\\manuscripts\\COMPLETE_RESEARCH_MASTER_DOCUMENTATION.html
"""

import os
import glob

ROOT_DIR = r"E:\software\acoustic-surveillance"
MANUSCRIPTS_DIR = os.path.join(ROOT_DIR, "manuscripts")
RESULTS_DIR = os.path.join(ROOT_DIR, "results")
HARDWARE_DIR = os.path.join(ROOT_DIR, "hardware")
DOCS_DIR = os.path.join(ROOT_DIR, "docs")
os.makedirs(MANUSCRIPTS_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)

# List of all key documentation files to merge in logical sequence
doc_files = [
    ("PART 1: PROJECT VISION, ARCHITECTURE & HARDWARE WIRING", os.path.join(ROOT_DIR, "README.md")),
    ("SYSTEM ARCHITECTURE & SOLAR GSM PROTOCOL", os.path.join(ROOT_DIR, "system_architecture.md")),
    ("HARDWARE WIRING GUIDE", os.path.join(HARDWARE_DIR, "wiring_guide.md")),
    ("SOUND CLASSES TAXONOMY", os.path.join(ROOT_DIR, "sound_classes.md")),
    ("SUB-CLASSES TAXONOMY", os.path.join(ROOT_DIR, "sub_classes.md")),
    ("DISTANCE ATTENUATION PHYSICS", os.path.join(ROOT_DIR, "distance_handling.md")),
    ("PART 2: CHAPTER 1 - INTRODUCTION & RESEARCH MOTIVATION", os.path.join(ROOT_DIR, "thesis_chapter_1.md")),
    ("PART 3: CHAPTER 2 - FORMAL LITERATURE REVIEW (73 PAPERS, 6 DOMAINS)", os.path.join(ROOT_DIR, "literature_review.md")),
    ("PART 4: CHAPTER 3 - DATASET METHODOLOGY, QUALITY CONTROL, SPEECH PURGING, PHYSICS SYNTHESIS & ISO 9613-2 AUGMENTATION", os.path.join(RESULTS_DIR, "dataset_methodology_detailed_report.md")),
    ("PART 5: CHAPTER 4 - TINYML SE-DS-CNN MODEL EVALUATION & EXPERIMENTAL RESULTS", os.path.join(RESULTS_DIR, "model_evaluation_report.md")),
    ("PART 6: HARDWARE POWER BUDGET, SOLAR HARVESTING EQUILIBRIUM & HT7333-1 CIRCUITRY", os.path.join(HARDWARE_DIR, "power_budget_guide.md")),
    ("PART 7: IP67 PETG WEATHERPROOF CAMOUFLAGED 3D ENCLOSURE DESIGN", os.path.join(HARDWARE_DIR, "enclosure_3d_design_guide.md")),
    ("PART 8: FIELD VERIFICATION, DISTANCE PLAYBACK TESTING & CELLULAR CSQ PROTOCOL", os.path.join(HARDWARE_DIR, "field_testing_protocol.md")),
    ("PART 9: CHAPTER 5 - CONCLUSION & FUTURE RESEARCH SCOPE", os.path.join(ROOT_DIR, "thesis_chapter_5.md")),
    ("PART 10: PROJECT PROGRESS TRACKER & TASK CHECKLIST", os.path.join(ROOT_DIR, "progress_tracker.md"))
]

master_lines = []
master_lines.append("# COMPLETE RESEARCH MASTER DOCUMENTATION")
master_lines.append("## EDGE AI-POWERED FOREST ACOUSTIC THREAT SURVEILLANCE SYSTEM USING TINYML SE-DS-CNN ON ESP32-S3 MICROCONTROLLERS")
master_lines.append("**Author / Lead Researcher**: Academic Research Team  ")
master_lines.append("**Hardware Target**: ESP32-S3 Dual-Core LX7 @ 240MHz | INMP441 I2S Mic | SIM800L GSM | Neo-6M GPS  ")
master_lines.append("**Dataset Scale**: 5,200 Clean 16kHz WAV Files (200 Clips/Class across 26 Classes)  ")
master_lines.append("**Neural Model**: Squeeze-and-Excitation 2D Depthwise-Separable CNN (27 KB INT8, PCEN Features)  \n")
master_lines.append("="*80 + "\n")

for section_title, filepath in doc_files:
    if os.path.exists(filepath):
        master_lines.append(f"\n\n# ==========================================================================")
        master_lines.append(f"# {section_title}")
        master_lines.append(f"# ==========================================================================\n")
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        master_lines.append(content)
        master_lines.append("\n\n" + "-"*80)

master_md = "\n".join(master_lines)

# Write Master MD
master_md_path = os.path.join(MANUSCRIPTS_DIR, "COMPLETE_RESEARCH_MASTER_DOCUMENTATION.md")
with open(master_md_path, 'w', encoding='utf-8') as f:
    f.write(master_md)

# Write Master HTML & DOC
master_html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>COMPLETE RESEARCH MASTER DOCUMENTATION</title>
<style>
body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.7; padding: 40px; max-width: 1050px; margin: auto; color: #1a202c; font-size: 11pt; }}
h1 {{ color: #002b49; border-bottom: 3px solid #002b49; padding-bottom: 10px; margin-top: 45px; font-size: 20pt; }}
h2 {{ color: #1a365d; margin-top: 30px; border-bottom: 1px solid #cbd5e0; padding-bottom: 6px; font-size: 15pt; }}
h3 {{ color: #2c5282; font-size: 13pt; }}
table {{ border-collapse: collapse; width: 100%; margin: 25px 0; font-size: 10.5pt; }}
th, td {{ border: 1px solid #718096; padding: 9px; text-align: left; }}
th {{ background-color: #ebf8ff; color: #1a365d; font-weight: bold; }}
code {{ background-color: #edf2f7; padding: 2px 5px; border-radius: 4px; font-family: Consolas, monospace; font-size: 10pt; }}
blockquote {{ border-left: 4px solid #2b6cb0; padding-left: 15px; margin-left: 0; color: #4a5568; font-style: italic; }}
img {{ max-width: 100%; height: auto; border: 1px solid #cbd5e0; border-radius: 4px; margin: 20px 0; }}
.header-box {{ background-color: #f7fafc; border: 2px solid #cbd5e0; padding: 20px; border-radius: 8px; margin-bottom: 30px; }}
</style>
</head>
<body>
<div class="header-box">
{master_md[:1500].replace('# ', '<h1>').replace('## ', '<h2>').replace('**', '<b>').replace('\n', '<br>')}
</div>
<hr>
{master_md.replace('# ', '<h1>').replace('## ', '<h2>').replace('### ', '<h3>').replace('\n\n', '<br><br>')}
</body>
</html>
"""

master_doc_path = os.path.join(MANUSCRIPTS_DIR, "COMPLETE_RESEARCH_MASTER_DOCUMENTATION.doc")
master_html_path = os.path.join(MANUSCRIPTS_DIR, "COMPLETE_RESEARCH_MASTER_DOCUMENTATION.html")

with open(master_html_path, 'w', encoding='utf-8') as f:
    f.write(master_html_content)
with open(master_doc_path, 'w', encoding='utf-8') as f:
    f.write(master_html_content)

print("COMPLETE RESEARCH MASTER DOCUMENTATION GENERATED (MD, DOC, HTML)!")

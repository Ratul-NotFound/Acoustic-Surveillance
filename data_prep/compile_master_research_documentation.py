"""
compile_master_research_documentation.py
──────────────────────────────────────────
Compiles ALL project documentation files into ONE SINGLE, EXTREMELY DETAILED MASTER RESEARCH DOCUMENT
using Python's `markdown` library for 100% clean, professional academic formatting without raw markdown symbols (#, ---, **).
"""

import os
import markdown

ROOT_DIR = r"E:\software\acoustic-surveillance"
MANUSCRIPTS_DIR = os.path.join(ROOT_DIR, "manuscripts")
RESULTS_DIR = os.path.join(ROOT_DIR, "results")
HARDWARE_DIR = os.path.join(ROOT_DIR, "hardware")
DOCS_DIR = os.path.join(ROOT_DIR, "docs")
os.makedirs(MANUSCRIPTS_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)

doc_files = [
    ("PART 1: PROJECT VISION, ARCHITECTURE & HARDWARE WIRING", os.path.join(DOCS_DIR, "README.md")),
    ("SYSTEM ARCHITECTURE & SOLAR GSM PROTOCOL", os.path.join(DOCS_DIR, "system_architecture.md")),
    ("HARDWARE WIRING GUIDE", os.path.join(DOCS_DIR, "wiring_guide.md")),
    ("SOUND CLASSES TAXONOMY", os.path.join(DOCS_DIR, "sound_classes.md")),
    ("SUB-CLASSES TAXONOMY", os.path.join(DOCS_DIR, "sub_classes.md")),
    ("DISTANCE ATTENUATION PHYSICS", os.path.join(DOCS_DIR, "distance_handling.md")),
    ("PART 2: CHAPTER 1 - INTRODUCTION & RESEARCH MOTIVATION", os.path.join(DOCS_DIR, "thesis_chapter_1.md")),
    ("PART 3: CHAPTER 2 - FORMAL LITERATURE REVIEW (73 PAPERS, 6 DOMAINS)", os.path.join(DOCS_DIR, "literature_review.md")),
    ("PART 4: CHAPTER 3 - DATASET METHODOLOGY, QUALITY CONTROL, SPEECH PURGING, PHYSICS SYNTHESIS & ISO 9613-2 AUGMENTATION", os.path.join(DOCS_DIR, "dataset_methodology_detailed_report.md")),
    ("PART 5: CHAPTER 4 - TINYML SE-DS-CNN MODEL EVALUATION & EXPERIMENTAL RESULTS", os.path.join(DOCS_DIR, "model_evaluation_report.md")),
    ("PART 6: HARDWARE POWER BUDGET, SOLAR HARVESTING EQUILIBRIUM & HT7333-1 CIRCUITRY", os.path.join(DOCS_DIR, "power_budget_guide.md")),
    ("PART 7: IP67 PETG WEATHERPROOF CAMOUFLAGED 3D ENCLOSURE DESIGN", os.path.join(DOCS_DIR, "enclosure_3d_design_guide.md")),
    ("PART 8: FIELD VERIFICATION, DISTANCE PLAYBACK TESTING & CELLULAR CSQ PROTOCOL", os.path.join(DOCS_DIR, "field_testing_protocol.md")),
    ("PART 9: CHAPTER 5 - CONCLUSION & FUTURE RESEARCH SCOPE", os.path.join(DOCS_DIR, "thesis_chapter_5.md")),
    ("PART 10: PROJECT PROGRESS TRACKER & TASK CHECKLIST", os.path.join(ROOT_DIR, "progress_tracker.md"))
]

master_md_parts = []
master_md_parts.append("# COMPLETE RESEARCH MASTER DOCUMENTATION\n")
master_md_parts.append("## EDGE AI-POWERED FOREST ACOUSTIC THREAT SURVEILLANCE SYSTEM USING TINYML SE-DS-CNN ON ESP32-S3 MICROCONTROLLERS\n")
master_md_parts.append("**Author / Lead Researcher**: Academic Research Team  \n")
master_md_parts.append("**Hardware Target**: ESP32-S3 Dual-Core LX7 @ 240MHz | INMP441 I2S Mic | SIM800L GSM | Neo-6M GPS  \n")
master_md_parts.append("**Dataset Scale**: 5,200 Clean 16kHz WAV Files (200 Clips/Class across 26 Classes)  \n")
master_md_parts.append("**Neural Model**: Squeeze-and-Excitation 2D Depthwise-Separable CNN (27 KB INT8, PCEN Features)  \n\n---\n")

for section_title, filepath in doc_files:
    if os.path.exists(filepath):
        master_md_parts.append(f"\n# {section_title}\n")
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        master_md_parts.append(content)
        master_md_parts.append("\n\n<div class='page-break'></div>\n")

master_md = "\n\n".join(master_md_parts)

# Write Master MD
master_md_path = os.path.join(MANUSCRIPTS_DIR, "COMPLETE_RESEARCH_MASTER_DOCUMENTATION.md")
with open(master_md_path, 'w', encoding='utf-8') as f:
    f.write(master_md)

# Convert Markdown to Clean HTML using markdown library
html_body = markdown.markdown(master_md, extensions=['tables', 'fenced_code', 'nl2br'])

styled_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>COMPLETE RESEARCH MASTER DOCUMENTATION</title>
<style>
@page {{
    size: A4;
    margin: 1in;
}}
body {{
    font-family: 'Segoe UI', Arial, sans-serif;
    line-height: 1.65;
    color: #1f2937;
    background-color: #ffffff;
    padding: 30px;
    max-width: 950px;
    margin: 0 auto;
    font-size: 11pt;
}}
.page-break {{
    page-break-before: always;
    margin-top: 40px;
}}
h1 {{
    color: #0f2b48;
    font-family: 'Calibri', 'Segoe UI', sans-serif;
    font-size: 22pt;
    font-weight: 700;
    border-bottom: 3px solid #0f2b48;
    padding-bottom: 8px;
    margin-top: 35px;
    margin-bottom: 15px;
    line-height: 1.25;
}}
h2 {{
    color: #1e4265;
    font-family: 'Calibri', 'Segoe UI', sans-serif;
    font-size: 15pt;
    font-weight: 600;
    border-bottom: 1.5px solid #d0d7de;
    padding-bottom: 5px;
    margin-top: 28px;
    margin-bottom: 12px;
}}
h3 {{
    color: #2b5c8f;
    font-family: 'Calibri', 'Segoe UI', sans-serif;
    font-size: 13pt;
    font-weight: 600;
    margin-top: 20px;
    margin-bottom: 8px;
}}
p {{
    margin-top: 0;
    margin-bottom: 12px;
    text-align: justify;
}}
ul, ol {{
    margin-top: 0;
    margin-bottom: 14px;
    padding-left: 24px;
}}
li {{
    margin-bottom: 4px;
}}
table {{
    border-collapse: collapse;
    width: 100%;
    margin: 20px 0;
    font-size: 10pt;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}}
th {{
    background-color: #0f2b48;
    color: #ffffff;
    font-weight: 600;
    padding: 10px 12px;
    text-align: left;
    border: 1px solid #0f2b48;
}}
td {{
    padding: 8px 12px;
    border: 1px solid #d0d7de;
    vertical-align: top;
}}
tr:nth-child(even) {{
    background-color: #f8fafc;
}}
code {{
    background-color: #f1f5f9;
    color: #0f172a;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 9.5pt;
    border: 1px solid #e2e8f0;
}}
pre {{
    background-color: #f8fafc;
    border: 1px solid #cbd5e1;
    padding: 14px;
    border-radius: 6px;
    overflow-x: auto;
    font-size: 9.5pt;
}}
pre code {{
    background-color: transparent;
    padding: 0;
    border: none;
}}
blockquote {{
    border-left: 4px solid #1e4265;
    background-color: #f0f4f8;
    margin: 16px 0;
    padding: 10px 18px;
    color: #334155;
    font-style: italic;
}}
hr {{
    border: none;
    border-top: 2px solid #e2e8f0;
    margin: 30px 0;
}}
img {{
    max-width: 100%;
    height: auto;
    display: block;
    margin: 20px auto;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
}}
</style>
</head>
<body>
{html_body}
</body>
</html>
"""

master_doc_path = os.path.join(MANUSCRIPTS_DIR, "COMPLETE_RESEARCH_MASTER_DOCUMENTATION.doc")
master_html_path = os.path.join(MANUSCRIPTS_DIR, "COMPLETE_RESEARCH_MASTER_DOCUMENTATION.html")

with open(master_html_path, 'w', encoding='utf-8') as f:
    f.write(styled_html)
with open(master_doc_path, 'w', encoding='utf-8') as f:
    f.write(styled_html)

print("COMPLETE MASTER RESEARCH DOCUMENTATION SUCCESSFULLY COMPILED WITH CLEAN PROFESSIONAL HTML/DOC FORMATTING!")

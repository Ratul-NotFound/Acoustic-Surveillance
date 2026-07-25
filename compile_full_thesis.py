"""
compile_full_thesis.py
───────────────────────
Compiles all 5 thesis chapters into a publication-grade MS Word & HTML document
using Python's `markdown` library for 100% clean formatting without raw markdown symbols (#, ---, **).
"""

import os
import markdown

ROOT_DIR = r"E:\software\acoustic-surveillance"
MANUSCRIPTS_DIR = os.path.join(ROOT_DIR, "manuscripts")
RESULTS_DIR = os.path.join(ROOT_DIR, "results")
DOCS_DIR = os.path.join(ROOT_DIR, "docs")
os.makedirs(MANUSCRIPTS_DIR, exist_ok=True)

ch1_file = os.path.join(ROOT_DIR, "docs", "thesis_chapter_1.md")
if not os.path.exists(ch1_file):
    ch1_file = os.path.join(ROOT_DIR, "thesis_chapter_1.md")

ch2_file = os.path.join(ROOT_DIR, "docs", "literature_review.md")
ch3_file = os.path.join(ROOT_DIR, "docs", "dataset_methodology_detailed_report.md")
ch4_file = os.path.join(ROOT_DIR, "docs", "model_evaluation_report.md")

ch5_file = os.path.join(ROOT_DIR, "docs", "thesis_chapter_5.md")
if not os.path.exists(ch5_file):
    ch5_file = os.path.join(ROOT_DIR, "thesis_chapter_5.md")

chapters = [
    ("Chapter 1: Introduction & Research Motivation", ch1_file),
    ("Chapter 2: Literature Review & State-of-the-Art Analysis", ch2_file),
    ("Chapter 3: Methodology & Dataset Engineering", ch3_file),
    ("Chapter 4: Model Evaluation & Experimental Results", ch4_file),
    ("Chapter 5: Conclusion & Future Research Scope", ch5_file)
]

compiled_md_parts = []
compiled_md_parts.append("# MASTER THESIS MANUSCRIPT\n")
compiled_md_parts.append("## EDGE AI-POWERED FOREST ACOUSTIC THREAT SURVEILLANCE SYSTEM USING TINYML SE-DS-CNN ON ESP32-S3 MICROCONTROLLERS\n")
compiled_md_parts.append("**Degree**: Master of Science in Computer Science & Engineering  \n**Target Hardware**: ESP32-S3 Microcontroller (TinyML SE-DS-CNN + PCEN Features)  \n**Academic Year**: 2026  \n\n---\n")

for title, fpath in chapters:
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        compiled_md_parts.append(content)
        compiled_md_parts.append("\n\n<div class='page-break'></div>\n\n")

full_md = "\n\n".join(compiled_md_parts)

# Write MD
full_md_path = os.path.join(MANUSCRIPTS_DIR, "full_thesis_manuscript.md")
with open(full_md_path, 'w', encoding='utf-8') as f:
    f.write(full_md)

# Convert Markdown to Clean HTML using markdown library
html_body = markdown.markdown(full_md, extensions=['tables', 'fenced_code', 'nl2br'])

styled_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Master Thesis Manuscript - Acoustic Forest Surveillance</title>
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
    max-width: 900px;
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
    font-size: 24pt;
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
    font-size: 16pt;
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

full_doc_path = os.path.join(MANUSCRIPTS_DIR, "full_thesis_manuscript.doc")
full_html_path = os.path.join(MANUSCRIPTS_DIR, "full_thesis_manuscript.html")

with open(full_html_path, 'w', encoding='utf-8') as f:
    f.write(styled_html)
with open(full_doc_path, 'w', encoding='utf-8') as f:
    f.write(styled_html)

print("FULL THESIS MANUSCRIPT SUCCESSFULLY COMPILED WITH CLEAN PROFESSIONAL HTML/DOC FORMATTING!")

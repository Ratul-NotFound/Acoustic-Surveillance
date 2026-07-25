"""
compile_full_thesis.py
───────────────────────
Compiles all 5 thesis chapters (Chapters 1, 2, 3, 4, 5) into a single, cohesive,
formatted Master Thesis Manuscript (DOC, HTML, MD).

Outputs:
  - E:\\software\\acoustic-surveillance\\full_thesis_manuscript.md
  - E:\\software\\acoustic-surveillance\\full_thesis_manuscript.doc
  - E:\\software\\acoustic-surveillance\\full_thesis_manuscript.html
"""

import os

ROOT_DIR = r"E:\software\acoustic-surveillance"
RESULTS_DIR = os.path.join(ROOT_DIR, "results")

# Chapter files
ch1_file = os.path.join(ROOT_DIR, "thesis_chapter_1.md")
ch2_file = os.path.join(ROOT_DIR, "literature_review.md")
ch3_file = os.path.join(RESULTS_DIR, "dataset_methodology_detailed_report.md")
ch4_file = os.path.join(RESULTS_DIR, "model_evaluation_report.md")
ch5_file = os.path.join(ROOT_DIR, "thesis_chapter_5.md")

chapters = [
    ("Chapter 1: Introduction & Research Motivation", ch1_file),
    ("Chapter 2: Literature Review & State-of-the-Art Analysis", ch2_file),
    ("Chapter 3: Methodology & Dataset Engineering", ch3_file),
    ("Chapter 4: Model Evaluation & Experimental Results", ch4_file),
    ("Chapter 5: Conclusion & Future Research Scope", ch5_file)
]

compiled_text = []
compiled_text.append("# MASTER THESIS MANUSCRIPT")
compiled_text.append("## EDGE AI-POWERED FOREST ACOUSTIC THREAT SURVEILLANCE SYSTEM USING TINYML SE-DS-CNN ON ESP32-S3 MICROCONTROLLERS\n")
compiled_text.append("---\n")

for title, fpath in chapters:
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        compiled_text.append(content)
        compiled_text.append("\n\n---\n\n")

full_md = "\n".join(compiled_text)

# Write MD
full_md_path = os.path.join(ROOT_DIR, "full_thesis_manuscript.md")
with open(full_md_path, 'w', encoding='utf-8') as f:
    f.write(full_md)

# Write HTML & DOC
full_html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Master Thesis Manuscript - Acoustic Forest Surveillance</title>
<style>
body {{ font-family: 'Times New Roman', Times, serif; line-height: 1.8; padding: 40px; max-width: 1000px; margin: auto; color: #111; font-size: 12pt; }}
h1 {{ color: #002b49; border-bottom: 3px solid #002b49; padding-bottom: 10px; margin-top: 40px; font-family: 'Segoe UI', Arial, sans-serif; font-size: 22pt; }}
h2 {{ color: #1a365d; margin-top: 30px; border-bottom: 1px solid #cbd5e0; padding-bottom: 6px; font-family: 'Segoe UI', Arial, sans-serif; font-size: 16pt; }}
h3 {{ color: #2c5282; font-family: 'Segoe UI', Arial, sans-serif; font-size: 14pt; }}
table {{ border-collapse: collapse; width: 100%; margin: 25px 0; font-size: 11pt; }}
th, td {{ border: 1px solid #718096; padding: 10px; text-align: left; }}
th {{ background-color: #e2e8f0; color: #1a202c; font-weight: bold; }}
code {{ background-color: #edf2f7; padding: 2px 5px; border-radius: 4px; font-family: Consolas, monospace; font-size: 10pt; }}
blockquote {{ border-left: 4px solid #2b6cb0; padding-left: 15px; margin-left: 0; color: #4a5568; font-style: italic; }}
img {{ max-width: 100%; height: auto; border: 1px solid #cbd5e0; border-radius: 4px; margin: 20px 0; }}
</style>
</head>
<body>
{full_md.replace('# ', '<h1>').replace('## ', '<h2>').replace('### ', '<h3>').replace('\n\n', '<br><br>')}
</body>
</html>
"""

full_doc_path = os.path.join(ROOT_DIR, "full_thesis_manuscript.doc")
full_html_path = os.path.join(ROOT_DIR, "full_thesis_manuscript.html")

with open(full_html_path, 'w', encoding='utf-8') as f:
    f.write(full_html_content)
with open(full_doc_path, 'w', encoding='utf-8') as f:
    f.write(full_html_content)

print("FULL MASTER THESIS MANUSCRIPT MANIFEST GENERATED (MD, DOC, HTML)!")

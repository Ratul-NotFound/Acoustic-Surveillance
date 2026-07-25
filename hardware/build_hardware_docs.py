import os
import glob
import markdown

DOCS_DIR = r"E:\software\acoustic-surveillance\docs"

style_head = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<style>
body { font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.65; color: #1f2937; background: #fff; padding: 30px; max-width: 950px; margin: 0 auto; font-size: 11pt; }
h1 { color: #0f2b48; font-family: 'Calibri', 'Segoe UI', sans-serif; font-size: 22pt; font-weight: 700; border-bottom: 3px solid #0f2b48; padding-bottom: 8px; margin-top: 35px; margin-bottom: 15px; }
h2 { color: #1e4265; font-family: 'Calibri', 'Segoe UI', sans-serif; font-size: 15pt; font-weight: 600; border-bottom: 1.5px solid #d0d7de; padding-bottom: 5px; margin-top: 28px; margin-bottom: 12px; }
h3 { color: #2b5c8f; font-family: 'Calibri', 'Segoe UI', sans-serif; font-size: 13pt; font-weight: 600; margin-top: 20px; margin-bottom: 8px; }
p { margin-top: 0; margin-bottom: 12px; text-align: justify; }
ul, ol { margin-top: 0; margin-bottom: 14px; padding-left: 24px; }
li { margin-bottom: 4px; }
table { border-collapse: collapse; width: 100%; margin: 20px 0; font-size: 10pt; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
th { background-color: #0f2b48; color: #ffffff; font-weight: 600; padding: 10px 12px; text-align: left; border: 1px solid #0f2b48; }
td { padding: 8px 12px; border: 1px solid #d0d7de; vertical-align: top; }
tr:nth-child(even) { background-color: #f8fafc; }
code { background-color: #f1f5f9; color: #0f172a; padding: 2px 6px; border-radius: 4px; font-family: 'Consolas', 'Courier New', monospace; font-size: 9.5pt; border: 1px solid #e2e8f0; }
pre { background-color: #f8fafc; border: 1px solid #cbd5e1; padding: 14px; border-radius: 6px; overflow-x: auto; font-size: 9.5pt; }
blockquote { border-left: 4px solid #1e4265; background-color: #f0f4f8; margin: 16px 0; padding: 10px 18px; color: #334155; font-style: italic; }
hr { border: none; border-top: 2px solid #e2e8f0; margin: 30px 0; }
img { max-width: 100%; height: auto; display: block; margin: 20px auto; border: 1px solid #cbd5e1; border-radius: 6px; }
</style>
</head>
<body>
"""

for md_path in glob.glob(os.path.join(DOCS_DIR, "*.md")):
    base_name = os.path.splitext(os.path.basename(md_path))[0]
    doc_path = os.path.join(DOCS_DIR, f"{base_name}.doc")
    html_path = os.path.join(DOCS_DIR, f"{base_name}.html")

    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    parsed_html = markdown.markdown(md_text, extensions=['tables', 'fenced_code', 'nl2br'])
    full_html = style_head + parsed_html + "</body></html>"

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write(full_html)

print("ALL INDIVIDUAL TOPIC DOC & HTML FILES CONVERTED TO CLEAN PROFESSIONAL FORMATTING!")

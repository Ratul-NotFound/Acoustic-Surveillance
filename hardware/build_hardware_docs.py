import os

hardware_dir = r"E:\software\acoustic-surveillance\hardware"

for fname in ['power_budget_guide', 'enclosure_3d_design_guide', 'field_testing_protocol']:
    md_file = os.path.join(hardware_dir, f"{fname}.md")
    doc_file = os.path.join(hardware_dir, f"{fname}.doc")
    html_file = os.path.join(hardware_dir, f"{fname}.html")

    with open(md_file, 'r', encoding='utf-8') as f:
        md_text = f.read()

    body_html = md_text.replace('# ', '<h1>').replace('## ', '<h2>').replace('### ', '<h3>').replace('\n\n', '<br><br>')
    full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{fname}</title>
<style>
body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; padding: 25px; color: #333; }}
h1 {{ color: #1a365d; border-bottom: 2px solid #2b6cb0; padding-bottom: 8px; }}
h2 {{ color: #2c5282; margin-top: 20px; border-bottom: 1px solid #cbd5e0; padding-bottom: 4px; }}
h3 {{ color: #2b6cb0; }}
table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
th, td {{ border: 1px solid #cbd5e0; padding: 10px; text-align: left; }}
th {{ background-color: #ebf8ff; color: #2c5282; }}
code {{ background-color: #edf2f7; padding: 2px 5px; border-radius: 4px; font-family: Consolas, monospace; }}
</style>
</head>
<body>
{body_html}
</body>
</html>
"""

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
    with open(doc_file, 'w', encoding='utf-8') as f:
        f.write(full_html)

print("All Hardware HTML and DOC exports generated successfully!")

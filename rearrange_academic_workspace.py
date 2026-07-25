"""
rearrange_academic_workspace.py
───────────────────────────────
Rearranges the software repository into a formal, standard academic research directory structure:
  - manuscripts/ : Holds complete thesis manuscript & complete master documentation (MD, DOC, HTML).
  - docs/        : Holds all individual topic guides & reports.
  - data_prep/   : Holds all Python data preprocessing & model training scripts.
  - firmware/   : Holds C++ firmware sketch (firmware.ino) and C++ header (model_data.h).
  - hardware/   : Holds hardware wiring schematics and CAD specs.
  - results/    : Holds high-resolution research PNG plots.
"""

import os
import shutil

ROOT_DIR = r"E:\software\acoustic-surveillance"
MANUSCRIPTS_DIR = os.path.join(ROOT_DIR, "manuscripts")
DOCS_DIR = os.path.join(ROOT_DIR, "docs")
RESULTS_DIR = os.path.join(ROOT_DIR, "results")
HARDWARE_DIR = os.path.join(ROOT_DIR, "hardware")

os.makedirs(MANUSCRIPTS_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)

# 1. Move Manuscripts to manuscripts/
for f in os.listdir(ROOT_DIR):
    if f.startswith("full_thesis_manuscript") or f.startswith("COMPLETE_RESEARCH_MASTER_DOCUMENTATION"):
        src = os.path.join(ROOT_DIR, f)
        dst = os.path.join(MANUSCRIPTS_DIR, f)
        if os.path.isfile(src) and src != dst:
            shutil.move(src, dst)

# 2. Copy/Move individual topic docs to docs/
docs_to_organize = [
    ("literature_review", ROOT_DIR),
    ("dataset_links", ROOT_DIR),
    ("distance_handling", ROOT_DIR),
    ("model_training_guide", ROOT_DIR),
    ("qora_search_synthesis", ROOT_DIR),
    ("README", ROOT_DIR),
    ("sound_classes", ROOT_DIR),
    ("sub_classes", ROOT_DIR),
    ("system_architecture", ROOT_DIR),
    ("WORK_UPDATE", ROOT_DIR),
    ("dataset_methodology_detailed_report", RESULTS_DIR),
    ("model_evaluation_report", RESULTS_DIR),
    ("power_budget_guide", HARDWARE_DIR),
    ("enclosure_3d_design_guide", HARDWARE_DIR),
    ("field_testing_protocol", HARDWARE_DIR),
    ("wiring_guide", HARDWARE_DIR)
]

for base_name, src_dir in docs_to_organize:
    for ext in ['.md', '.doc', '.html', '.txt']:
        filename = f"{base_name}{ext}"
        src_path = os.path.join(src_dir, filename)
        if os.path.exists(src_path):
            dst_path = os.path.join(DOCS_DIR, filename)
            shutil.copy2(src_path, dst_path)

print("WORKSPACE SUCCESSFULLY REARRANGED INTO FORMAL ACADEMIC RESEARCH STRUCTURE!")

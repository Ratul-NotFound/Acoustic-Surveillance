# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "scienceskillscommon",
#   "python-dotenv",
# ]
# [tool.uv.sources]
# scienceskillscommon = { path = "C:/Users/mhrat/.gemini/config/plugins/science/skills/scienceskillscommon" }
# ///

import sys
import types
import os
import tempfile

# Mock fcntl for Windows compatibility
if os.name == 'nt':
    mock_fcntl = types.ModuleType('fcntl')
    mock_fcntl.LOCK_EX = 1
    mock_fcntl.LOCK_SH = 2
    mock_fcntl.LOCK_NB = 4
    mock_fcntl.LOCK_UN = 8
    def mock_flock(fd, op):
        pass
    mock_fcntl.flock = mock_flock
    sys.modules['fcntl'] = mock_fcntl

# Monkeypatch RateLimiter lock file path on Windows
from science_skills.skills.scienceskillscommon import http_client
original_init = http_client._RateLimiter.__init__
def patched_init(self, hostname: str, qps: float):
    original_init(self, hostname, qps)
    self._lock_file = os.path.join(tempfile.gettempdir(), f"science-skills-{hostname}.lock")
http_client._RateLimiter.__init__ = patched_init

import runpy

if len(sys.argv) < 2:
    print("Usage: python run_science_skill.py <script_path> [args...]")
    sys.exit(1)

script_path = sys.argv[1]
# Shift sys.argv so the target script sees the correct arguments
sys.argv = sys.argv[1:]

print(f"Running script: {script_path} with args {sys.argv[1:]}")
runpy.run_path(script_path, run_name="__main__")

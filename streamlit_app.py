"""
Streamlit Cloud Entrypoint for AI Resume Analyzer
Author: Dilkhush Raj (https://github.com/Dilkhush144)
"""

import runpy
from pathlib import Path

# Execute main application file
app_path = Path(__file__).parent / "app.py"
runpy.run_path(str(app_path), run_name="__main__")

from .chat import Chat, Message
from .ui import UI

__all__ = ["Chat", "Message", "UI"]

import subprocess
import sys
from pathlib import Path

def main():
    main_file = Path(__file__).parent / "main.py"
    cmd = ["streamlit", "run", str(main_file)]
    subprocess.run(cmd)
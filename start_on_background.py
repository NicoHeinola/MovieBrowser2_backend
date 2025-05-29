import subprocess
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

subprocess.Popen("start_on_background.bat", cwd=script_dir, shell=True)

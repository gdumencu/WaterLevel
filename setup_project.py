import os
import subprocess
import sys

def run(cmd):
    print(f"Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

# Clone repo if not already present
repo_url = input("Enter GitHub repo URL (or leave blank if already cloned): ").strip()
if repo_url:
    run(f"git clone {repo_url}")

# Backend setup
if os.path.isdir("backend"):
    os.chdir("backend")
    run("python -m venv venv")
    if sys.platform == "win32":
        run(r"venv\Scripts\activate && pip install -r requirements.txt")
    else:
        run("source venv/bin/activate && pip install -r requirements.txt")
    os.chdir("..")

# Frontend setup
if os.path.isdir("frontend"):
    os.chdir("frontend")
    run("npm install")
    os.chdir("..")

print("Backend and frontend dependencies installed.")

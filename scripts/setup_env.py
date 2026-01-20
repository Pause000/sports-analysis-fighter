import sys
import subprocess
import os

def install_requirements(req_file="requirements.txt"):
    """
    Check if required packages are installed.
    If not, install them using pip from requirements.txt.
    
    This function handles:
    1. Checking for existence of requirements file.
    2. Verifying critical imports (flask, pandas, etc.).
    3. Auto-installing dependencies via subprocess if missing.
    4. Restarting the application to load new packages.
    """
    if not os.path.exists(req_file):
        return

    try:
        # Try importing critical packages to see if they exist
        import flask
        import pandas
        import joblib
        import sentence_transformers
        import node2vec
    except ImportError:
        print("📦 Required packages not found. Installing from requirements.txt...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_file])
            print("✅ Dependencies installed successfully! Restarting application...")
            os.execv(sys.executable, [sys.executable] + sys.argv)
        except Exception as e:
            print(f"❌ Failed to install dependencies: {e}")
            sys.exit(1)

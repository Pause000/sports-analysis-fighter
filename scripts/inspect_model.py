import joblib
import os

MODEL_PATH = 'sports_chatbot_model50.joblib'

if os.path.exists(MODEL_PATH):
    try:
        artifacts = joblib.load(MODEL_PATH)
        print("Keys in artifacts:", list(artifacts.keys()))
        for key in artifacts:
            if key != 'final_model': # Model might be too big to print
                print(f"{key}: {artifacts[key]}")
            else:
                print(f"{key}: {type(artifacts[key])}")
    except Exception as e:
        print(f"Error loading {MODEL_PATH}: {e}")
else:
    print(f"File not found: {MODEL_PATH}")

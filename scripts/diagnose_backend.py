import joblib
import os
import json
import pandas as pd
import numpy as np

MODEL_PATH = 'sports_chatbot_model50.joblib'

def test_load():
    if not os.path.exists(MODEL_PATH):
        print(f"Error: {MODEL_PATH} not found")
        return
    
    try:
        artifacts = joblib.load(MODEL_PATH)
        print("SUCCESS: Artifacts loaded successfully")
        print("Keys:", list(artifacts.keys()))
        
        input_features = artifacts.get('input_features')
        print("Input Features:", input_features)
        
        le_league = artifacts.get('le_league')
        if le_league:
            print("Leagues in LabelEncoder:", le_league.classes_)
            
    except Exception as e:
        print(f"ERROR: Error loading artifacts: {e}")

if __name__ == "__main__":
    test_load()

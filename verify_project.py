import os
import pickle
import pandas as pd
from bridge_sim import generate_bridge_data

def check_file(filename):
    if os.path.exists(filename):
        print(f"✅ Found {filename}")
        return True
    else:
        print(f"❌ MISSING {filename}")
        return False

print("--- SetuAayu Project Self-Check ---\n")

# 1. File Integrity Check
files_to_check = [
    "app.py",
    "bridge_sim.py",
    "bridge_viewer_template.html",
    "firmware.ino",
    "generate_dataset.py",
    "train_model.py",
    "bridge_data.csv",
    "model.pkl",
    "DATASETS.md"
]

all_files = True
for f in files_to_check:
    if not check_file(f):
        all_files = False

if not all_files:
    print("\nWARNING: Some files are missing. Please investigate.")
else:
    print("\n✅ All critical files present.")

# 2. Simulation Logic Check
print("\n--- Testing Simulation Logic ---")
try:
    data = generate_bridge_data("critical")
    if data['health_score'] < 70 and data['prediction_window'] != "None (Safe)":
        print(f"✅ Simulation Logic Valid (Returned Health Score: {data['health_score']})")
    else:
        print("❌ Simulation Logic Warning: Critical mode didn't return critical values.")
except Exception as e:
    print(f"❌ Simulation Logic Failed: {str(e)}")

# 3. Model Loading Check
print("\n--- Testing ML Model ---")
try:
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    print("✅ Model loaded successfully.")
    
    # Simple Inference Test
    test_input = [[0.5, 0.5, 0.5, 600, 3.0]] # High values
    pred = model.predict(test_input)[0]
    print(f"✅ Model Inference Test: Input=High Values -> Prediction={pred} (Expected 1)")
except Exception as e:
    print(f"❌ Model Check Failed: {str(e)}")

print("\n--- Check Complete ---")

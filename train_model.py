import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# 1. Load Data
print("Loading dataset...")
try:
    df = pd.read_csv("bridge_data.csv")
except FileNotFoundError:
    print("Error: 'bridge_data.csv' not found. Run 'generate_dataset.py' first.")
    exit()

# 2. Preprocessing
# Features
X = df[['vibration_x', 'vibration_y', 'vibration_z', 'strain', 'tilt']]
# Target (Convert 'critical'/'normal' to 1/0)
y = df['scenario'].apply(lambda x: 1 if x == 'critical' else 0)

# 3. Split Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Train Model
print(f"Training Random Forest on {len(X_train)} samples...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. Verify (Test)
print("\n--- Model Verification Results ---")
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Normal', 'Critical']))

# 6. Save Model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)
    
print("\n✅ Model saved to 'model.pkl'. Ready for app integration.")

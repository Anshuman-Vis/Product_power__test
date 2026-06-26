"""
ProductPower - ML Training Script
"""

import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import os

print("🚀 Training Food Risk Model...")

# Create models folder
os.makedirs("models", exist_ok=True)

# ===============================
# Generate synthetic training data
# ===============================
np.random.seed(42)
n = 1500

data = pd.DataFrame({
    "sugar": np.random.uniform(0, 50, n),
    "sodium": np.random.uniform(0, 1000, n),
    "saturated_fat": np.random.uniform(0, 20, n),
    "additives_count": np.random.randint(0, 8, n),
    "preservatives": np.random.randint(0, 5, n),
})

# Create risk score formula
risk_score = (
    data["sugar"] * 1.5 +
    data["sodium"] / 40 +
    data["saturated_fat"] * 2 +
    data["additives_count"] * 4 +
    data["preservatives"] * 3
)

# Convert to categories
data["risk_category"] = pd.cut(
    risk_score,
    bins=[0, 40, 70, 100, 200],
    labels=["Low", "Moderate", "High", "Very High"]
)

data = data.dropna()

# ===============================
# Prepare data
# ===============================
X = data[["sugar", "sodium", "saturated_fat", "additives_count", "preservatives"]]
y = data["risk_category"]

label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

# ===============================
# Train Model
# ===============================
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)

print(f"✅ Model Accuracy: {accuracy:.2f}")

# ===============================
# Save Models
# ===============================
joblib.dump(model, "models/food_risk_model.pkl")
joblib.dump(label_encoder, "models/risk_label_encoder.pkl")

print("✅ Models saved in /models folder")
print("🎉 Training Complete!")
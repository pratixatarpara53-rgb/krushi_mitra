"""
train_model.py – KhedutMitra ML Module
Trains a Random Forest Regressor to predict crop yield (quintals/hectare)
based on agronomic inputs. Run once to generate 'crop_yield_model.pkl'.

Usage:
    python train_model.py
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import json
import os

# ---------------------------------------------------------------------------
# 1. Generate a realistic synthetic training dataset
# ---------------------------------------------------------------------------
np.random.seed(42)
N = 3000  # number of training samples

CROP_BASE_YIELD = {
    "Cotton":    20,
    "Groundnut": 18,
    "Wheat":     35,
    "Bajra":     22,
    "Maize":     40,
    "Cumin":     8,
    "Chilli":    90,
    "Onion":     200,
}

SOIL_FACTOR = {
    "Sandy":       0.80,
    "Sandy Loam":  0.95,
    "Loam":        1.05,
    "Clay Loam":   1.00,
    "Black Cotton":1.10,
}

SEASON_FACTOR = {
    "Kharif": 1.00,
    "Rabi":   1.05,
    "Zaid":   0.90,
}

IRRIGATION_FACTOR = {
    "Rainfed":  0.75,
    "Flood":    0.90,
    "Drip":     1.20,
    "Sprinkler":1.10,
}

rows = []
for _ in range(N):
    crop      = np.random.choice(list(CROP_BASE_YIELD.keys()))
    soil      = np.random.choice(list(SOIL_FACTOR.keys()))
    season    = np.random.choice(list(SEASON_FACTOR.keys()))
    irrigation= np.random.choice(list(IRRIGATION_FACTOR.keys()))
    rainfall  = np.random.uniform(200, 1200)   # mm
    temperature= np.random.uniform(15, 42)     # °C
    fertilizer = np.random.uniform(40, 200)    # kg/ha NPK

    # Rainfall modifier (optimal zone differs per crop)
    rain_opt = 600.0
    rain_mod = 1.0 - abs(rainfall - rain_opt) / 3000.0

    # Temperature modifier
    temp_opt = 28.0
    temp_mod = 1.0 - abs(temperature - temp_opt) / 80.0

    # Fertiliser modifier
    fert_mod = 0.85 + (fertilizer / 200.0) * 0.25

    base = CROP_BASE_YIELD[crop]
    yield_val = (
        base
        * SOIL_FACTOR[soil]
        * SEASON_FACTOR[season]
        * IRRIGATION_FACTOR[irrigation]
        * rain_mod
        * temp_mod
        * fert_mod
    )
    yield_val = max(1.0, yield_val + np.random.normal(0, base * 0.05))

    rows.append({
        "crop": crop,
        "soil": soil,
        "season": season,
        "irrigation": irrigation,
        "rainfall": round(rainfall, 1),
        "temperature": round(temperature, 1),
        "fertilizer": round(fertilizer, 1),
        "yield": round(yield_val, 2),
    })

df = pd.DataFrame(rows)

# ---------------------------------------------------------------------------
# 2. Encode categoricals
# ---------------------------------------------------------------------------
encoders = {}
cat_cols = ["crop", "soil", "season", "irrigation"]
for col in cat_cols:
    le = LabelEncoder()
    df[col + "_enc"] = le.fit_transform(df[col])
    encoders[col] = {cls: int(i) for i, cls in enumerate(le.classes_)}

feature_cols = [c + "_enc" for c in cat_cols] + ["rainfall", "temperature", "fertilizer"]
X = df[feature_cols].values
y = df["yield"].values

# ---------------------------------------------------------------------------
# 3. Train / test split & model training
# ---------------------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=200, max_depth=12, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mae  = mean_absolute_error(y_test, y_pred)
r2   = r2_score(y_test, y_pred)
print(f"[ML] Training complete — MAE: {mae:.2f} q/ha  |  R² score: {r2:.4f}")

# ---------------------------------------------------------------------------
# 4. Save model and encoder map
# ---------------------------------------------------------------------------
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/crop_yield_model.pkl")
with open("models/encoders.json", "w") as f:
    json.dump(encoders, f, indent=2)

print("[ML] Model saved  ->  models/crop_yield_model.pkl")
print("[ML] Encoders saved ->  models/encoders.json")

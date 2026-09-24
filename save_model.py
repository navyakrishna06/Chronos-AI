import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# Load Dataset
df = pd.read_csv("datasets/processed/ai4i_clean.csv")

# Encode Type
encoder = LabelEncoder()
df["Type"] = encoder.fit_transform(df["Type"])

# Features
X = df[[
    "Type",
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]"
]]

# Target
y = df["Machine failure"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train Model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Save Model
joblib.dump(model, "machine_failure_model.pkl")

print("Model Saved Successfully")
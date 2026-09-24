import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load cleaned dataset
df = pd.read_csv("datasets/processed/ai4i_clean.csv")

# Features
X = df[[
    "Type",
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]"
]]

# Convert categorical data
X = pd.get_dummies(X)

# Target
y = df["Machine failure"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create Model
model = RandomForestClassifier(random_state=42)

# Train Model
model.fit(X_train, y_train)

print("✅ Model Training Completed Successfully")
print("Training Samples:", len(X_train))
print("Testing Samples:", len(X_test))
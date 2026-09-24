import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.preprocessing import LabelEncoder

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score

# Load Dataset
df = pd.read_csv("datasets/processed/ai4i_clean.csv")

# Encode Type Column
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

# Split Dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Optimized Random Forest
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    random_state=42
)

# Train
model.fit(X_train, y_train)

# Predict
prediction = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, prediction)

print("\n===== OPTIMIZED RANDOM FOREST =====")

print(f"\nAccuracy : {accuracy*100:.2f}%")
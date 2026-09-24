import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load dataset
df = pd.read_csv("datasets/processed/ai4i_clean.csv")

# Convert Type into numerical values
df["Type"] = df["Type"].map({"L":0,"M":1,"H":2})

# Input Features
X = df[
[
    "Type",
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]"
]
]

# Target
Y = df["Machine failure"]

# Split Dataset
X_train, X_test, Y_train, Y_test = train_test_split(
    X,
    Y,
    test_size=0.2,
    random_state=42
)

# Create Model
model = RandomForestClassifier(random_state=42)

# Train Model
model.fit(X_train, Y_train)

# Prediction
Y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(Y_test, Y_pred)

print("Model Trained Successfully")
print("Accuracy:", round(accuracy*100,2),"%")

print("\nClassification Report\n")
print(classification_report(Y_test,Y_pred))
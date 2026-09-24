import joblib
import pandas as pd

# Load trained model
model = joblib.load("machine_failure_model.pkl")

# Sample machine data
sample_data = pd.DataFrame([{
    "Type": 1,
    "Air temperature [K]": 298.2,
    "Process temperature [K]": 308.5,
    "Rotational speed [rpm]": 1550,
    "Torque [Nm]": 42.0,
    "Tool wear [min]": 20
}])

# Predict
prediction = model.predict(sample_data)

print("\n========== PREDICTION RESULT ==========\n")

if prediction[0] == 1:
    print("⚠️ Machine Failure Predicted")
else:
    print("✅ No Machine Failure Predicted")
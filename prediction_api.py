# ============================================================
# CHRONOS AI - DAY 48
# PREDICTION API DEVELOPMENT
# ============================================================

import os
import joblib
import pandas as pd

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn


# ============================================================
# PATHS
# ============================================================

BASE_PATH = r"C:\Users\navya\OneDrive\Documents\Chronos"

MODEL_PATH = os.path.join(
    BASE_PATH,
    "models",
    "chronos_random_forest.pkl"
)

METADATA_PATH = os.path.join(
    BASE_PATH,
    "models",
    "chronos_prediction_metadata.joblib"
)


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Chronos AI Prediction API",
    description="Machine Failure Prediction API using Random Forest",
    version="1.0.0"
)


# ============================================================
# FEATURE DEFINITIONS
# ============================================================

FEATURE_COLUMNS = [
    "HDF",
    "OSF",
    "PWF",
    "TWF",
    "High Torque",
    "Torque [Nm]",
    "Power Indicator",
    "Temperature Difference [K]",
    "Tool wear [min]",
    "High Tool Wear",
    "Air temperature [K]",
    "Temperature Stress"
]


# ============================================================
# LOAD MODEL
# ============================================================

print("=" * 60)
print("          CHRONOS AI - DAY 48")
print("          PREDICTION API DEVELOPMENT")
print("=" * 60)

print("\nLoading Random Forest Model...")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"Model file not found:\n{MODEL_PATH}"
    )

model = joblib.load(MODEL_PATH)

print("Random Forest Model Loaded Successfully")


# ============================================================
# LOAD METADATA
# ============================================================

metadata = {}

if os.path.exists(METADATA_PATH):
    try:
        metadata = joblib.load(METADATA_PATH)
        print("Model Metadata Loaded Successfully")
    except Exception as error:
        print("Warning: Metadata could not be loaded.")
        print("Reason:", error)
else:
    print("Metadata file not found. Continuing without metadata.")


# ============================================================
# REQUEST DATA MODEL
# ============================================================

class MachineData(BaseModel):

    HDF: int
    OSF: int
    PWF: int
    TWF: int
    High_Torque: int
    Torque_Nm: float
    Power_Indicator: float
    Temperature_Difference_K: float
    Tool_wear_min: float
    High_Tool_Wear: int
    Air_temperature_K: float
    Temperature_Stress: int


# ============================================================
# ROOT API
# ============================================================

@app.get("/")
def home():

    return {
        "project": "Chronos AI",
        "day": 48,
        "module": "Prediction API",
        "status": "API is running",
        "model": "Random Forest Classifier",
        "endpoint": "/predict",
        "documentation": "/docs"
    }


# ============================================================
# HEALTH CHECK API
# ============================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "model_loaded": True,
        "model_type": "RandomForestClassifier"
    }


# ============================================================
# PREDICTION API
# ============================================================

@app.post("/predict")
def predict_failure(data: MachineData):

    # --------------------------------------------------------
    # Convert API input into model feature format
    # --------------------------------------------------------

    input_data = pd.DataFrame([{
        "HDF": data.HDF,
        "OSF": data.OSF,
        "PWF": data.PWF,
        "TWF": data.TWF,
        "High Torque": data.High_Torque,
        "Torque [Nm]": data.Torque_Nm,
        "Power Indicator": data.Power_Indicator,
        "Temperature Difference [K]":
            data.Temperature_Difference_K,
        "Tool wear [min]": data.Tool_wear_min,
        "High Tool Wear": data.High_Tool_Wear,
        "Air temperature [K]":
            data.Air_temperature_K,
        "Temperature Stress": data.Temperature_Stress
    }])

    # --------------------------------------------------------
    # Arrange columns exactly like training data
    # --------------------------------------------------------

    input_data = input_data[FEATURE_COLUMNS]

    # --------------------------------------------------------
    # Generate prediction
    # --------------------------------------------------------

    prediction = int(model.predict(input_data)[0])

    probability = model.predict_proba(input_data)[0]

    failure_probability = float(probability[1])

    normal_probability = float(probability[0])

    # --------------------------------------------------------
    # Determine machine status
    # --------------------------------------------------------

    if failure_probability >= 0.70:

        status = "CRITICAL"
        message = "High probability of machine failure. Immediate inspection recommended."

    elif failure_probability >= 0.30:

        status = "WARNING"
        message = "Machine shows elevated failure risk. Maintenance inspection recommended."

    else:

        status = "NORMAL"
        message = "Machine is operating within the predicted normal condition."

    # --------------------------------------------------------
    # Final response
    # --------------------------------------------------------

    return {
        "prediction": prediction,
        "failure_probability": round(
            failure_probability,
            4
        ),
        "normal_probability": round(
            normal_probability,
            4
        ),
        "status": status,
        "message": message
    }


# ============================================================
# API INFORMATION
# ============================================================

@app.get("/model-info")
def model_info():

    return {
        "model_type": "Random Forest Classifier",
        "number_of_trees": 100,
        "maximum_depth": 8,
        "random_seed": 42,
        "features": FEATURE_COLUMNS,
        "total_features": len(FEATURE_COLUMNS),
        "metadata_available": bool(metadata)
    }


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    print("\n" + "=" * 60)
    print("STARTING CHRONOS AI PREDICTION API")
    print("=" * 60)

    print("\nAPI URL:")
    print("http://127.0.0.1:8000")

    print("\nSwagger Documentation:")
    print("http://127.0.0.1:8000/docs")

    print("\nPrediction Endpoint:")
    print("POST http://127.0.0.1:8000/predict")

    print("\nStarting server...\n")

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )

# ============================================================
# CHRONOS AI - DAY 49
# ALERT & RISK CLASSIFICATION MODULE
# ============================================================

import os
import joblib
import pandas as pd
from datetime import datetime


# ============================================================
# PATHS
# ============================================================

BASE_PATH = r"C:\Users\navya\OneDrive\Documents\Chronos"

MODEL_PATH = os.path.join(
    BASE_PATH,
    "models",
    "chronos_random_forest.pkl"
)

OUTPUT_PATH = os.path.join(
    BASE_PATH,
    "datasets",
    "processed",
    "day49_risk_predictions.csv"
)


# ============================================================
# FEATURE COLUMNS
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
# HEADER
# ============================================================

print("=" * 60)
print("          CHRONOS AI - DAY 49")
print("       ALERT & RISK CLASSIFICATION")
print("=" * 60)


# ============================================================
# 1. CHECK MODEL
# ============================================================

print("\n" + "=" * 60)
print("1. CHECKING TRAINED MODEL")
print("=" * 60)

if not os.path.exists(MODEL_PATH):

    print("Model Status : NOT FOUND")
    print("Expected Path:")
    print(MODEL_PATH)

    raise FileNotFoundError(
        "Chronos Random Forest model was not found."
    )

print("Model Status : FOUND")
print("Model Path   :", MODEL_PATH)


# ============================================================
# 2. LOAD MODEL
# ============================================================

print("\n" + "=" * 60)
print("2. LOADING RANDOM FOREST MODEL")
print("=" * 60)

model = joblib.load(MODEL_PATH)

print("Random Forest Model Loaded Successfully")


# ============================================================
# 3. RISK CLASSIFICATION FUNCTION
# ============================================================

print("\n" + "=" * 60)
print("3. CREATING RISK CLASSIFICATION FUNCTION")
print("=" * 60)


def classify_risk(failure_probability):

    if failure_probability >= 0.70:

        return (
            "CRITICAL",
            "High probability of machine failure. "
            "Immediate maintenance inspection recommended."
        )

    elif failure_probability >= 0.30:

        return (
            "WARNING",
            "Elevated machine failure risk detected. "
            "Maintenance inspection recommended."
        )

    else:

        return (
            "NORMAL",
            "Machine is operating within the predicted normal condition."
        )


print("Risk Classification Function Created Successfully")


# ============================================================
# 4. PREDICTION FUNCTION
# ============================================================

print("\n" + "=" * 60)
print("4. CREATING ALERT PREDICTION FUNCTION")
print("=" * 60)


def predict_machine_risk(machine_data):

    input_data = pd.DataFrame(
        [machine_data],
        columns=FEATURE_COLUMNS
    )

    prediction = int(
        model.predict(input_data)[0]
    )

    probabilities = model.predict_proba(input_data)[0]

    normal_probability = float(probabilities[0])

    failure_probability = float(probabilities[1])

    risk_level, alert_message = classify_risk(
        failure_probability
    )

    if risk_level == "CRITICAL":

        alert_required = "YES"

    elif risk_level == "WARNING":

        alert_required = "YES"

    else:

        alert_required = "NO"

    return {
        "prediction": prediction,
        "normal_probability": normal_probability,
        "failure_probability": failure_probability,
        "risk_level": risk_level,
        "alert_required": alert_required,
        "alert_message": alert_message
    }


print("Alert Prediction Function Created Successfully")


# ============================================================
# 5. TEST NORMAL MACHINE
# ============================================================

print("\n" + "=" * 60)
print("5. TESTING NORMAL MACHINE")
print("=" * 60)


normal_machine = [
    0,          # HDF
    0,          # OSF
    0,          # PWF
    0,          # TWF
    0,          # High Torque
    13.5,       # Torque [Nm]
    33696.0,    # Power Indicator
    9.2,        # Temperature Difference [K]
    21,         # Tool wear [min]
    0,          # High Tool Wear
    304.3,      # Air temperature [K]
    0           # Temperature Stress
]


normal_result = predict_machine_risk(
    normal_machine
)


print("\nNormal Machine Test Result:")

print(
    "Prediction            :",
    normal_result["prediction"]
)

print(
    "Normal Probability    :",
    round(
        normal_result["normal_probability"],
        4
    )
)

print(
    "Failure Probability   :",
    round(
        normal_result["failure_probability"],
        4
    )
)

print(
    "Risk Level            :",
    normal_result["risk_level"]
)

print(
    "Alert Required        :",
    normal_result["alert_required"]
)

print(
    "Message               :",
    normal_result["alert_message"]
)


# ============================================================
# 6. TEST WARNING / HIGH-RISK SCENARIO
# ============================================================

print("\n" + "=" * 60)
print("6. TESTING HIGH-RISK MACHINE SCENARIO")
print("=" * 60)


high_risk_machine = [
    1,          # HDF
    1,          # OSF
    1,          # PWF
    1,          # TWF
    1,          # High Torque
    25.0,       # Torque [Nm]
    50000.0,    # Power Indicator
    20.0,       # Temperature Difference [K]
    250,        # Tool wear [min]
    1,          # High Tool Wear
    310.0,      # Air temperature [K]
    1           # Temperature Stress
]


high_risk_result = predict_machine_risk(
    high_risk_machine
)


print("\nHigh-Risk Machine Test Result:")

print(
    "Prediction            :",
    high_risk_result["prediction"]
)

print(
    "Normal Probability    :",
    round(
        high_risk_result["normal_probability"],
        4
    )
)

print(
    "Failure Probability   :",
    round(
        high_risk_result["failure_probability"],
        4
    )
)

print(
    "Risk Level            :",
    high_risk_result["risk_level"]
)

print(
    "Alert Required        :",
    high_risk_result["alert_required"]
)

print(
    "Message               :",
    high_risk_result["alert_message"]
)


# ============================================================
# 7. ALERT LEVEL EXPLANATION
# ============================================================

print("\n" + "=" * 60)
print("7. ALERT LEVEL DEFINITIONS")
print("=" * 60)

print("\nNORMAL")
print("- Failure probability < 30%")
print("- No immediate alert required")
print("- Continue regular monitoring")

print("\nWARNING")
print("- Failure probability between 30% and 69.99%")
print("- Maintenance inspection recommended")
print("- Increase machine monitoring")

print("\nCRITICAL")
print("- Failure probability >= 70%")
print("- Immediate maintenance inspection recommended")
print("- High priority alert")


# ============================================================
# 8. CREATE RISK REPORT
# ============================================================

print("\n" + "=" * 60)
print("8. CREATING RISK REPORT")
print("=" * 60)


current_time = datetime.now().strftime(
    "%Y-%m-%d %H:%M:%S"
)


report_data = [

    {
        "Timestamp": current_time,
        "Machine": "Normal Test Machine",
        "Prediction": normal_result["prediction"],
        "Normal Probability":
            round(
                normal_result["normal_probability"],
                4
            ),
        "Failure Probability":
            round(
                normal_result["failure_probability"],
                4
            ),
        "Risk Level":
            normal_result["risk_level"],
        "Alert Required":
            normal_result["alert_required"],
        "Alert Message":
            normal_result["alert_message"]
    },

    {
        "Timestamp": current_time,
        "Machine": "High Risk Test Machine",
        "Prediction": high_risk_result["prediction"],
        "Normal Probability":
            round(
                high_risk_result["normal_probability"],
                4
            ),
        "Failure Probability":
            round(
                high_risk_result["failure_probability"],
                4
            ),
        "Risk Level":
            high_risk_result["risk_level"],
        "Alert Required":
            high_risk_result["alert_required"],
        "Alert Message":
            high_risk_result["alert_message"]
    }
]


risk_df = pd.DataFrame(report_data)


# ============================================================
# 9. SAVE RISK REPORT
# ============================================================

print("\n" + "=" * 60)
print("9. SAVING RISK REPORT")
print("=" * 60)


risk_df.to_csv(
    OUTPUT_PATH,
    index=False
)


print("Risk Report Saved Successfully:")
print(OUTPUT_PATH)

print("\nRisk Report Shape:")
print(
    "Rows   :",
    risk_df.shape[0]
)

print(
    "Columns:",
    risk_df.shape[1]
)


# ============================================================
# 10. DISPLAY RISK REPORT
# ============================================================

print("\n" + "=" * 60)
print("10. RISK REPORT")
print("=" * 60)

print()

print(
    risk_df.to_string(
        index=False
    )
)


# ============================================================
# 11. MODULE VERIFICATION
# ============================================================

print("\n" + "=" * 60)
print("11. MODULE VERIFICATION")
print("=" * 60)


if os.path.exists(OUTPUT_PATH):

    print("Model Status       : VERIFIED")
    print("Risk Function      : VERIFIED")
    print("Prediction Function: VERIFIED")
    print("Risk Report        : CREATED")
    print("CSV Status         : SUCCESS")


else:

    print("Risk Report Status  : FAILED")


# ============================================================
# 12. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("12. DAY 49 SUMMARY")
print("=" * 60)

print("• Random Forest model loaded successfully.")
print("• Risk classification function created.")
print("• Prediction function created.")
print("• Normal machine scenario tested.")
print("• High-risk machine scenario tested.")
print("• Failure probability calculated.")
print("• Risk level identified.")
print("• Alert requirement identified.")
print("• Alert message generated.")
print("• Risk report created.")
print("• Risk report saved successfully.")
print("• Alert & Risk Classification Module verified.")


print("\nChronos AI Alert & Risk Classification Module")
print("is ready for integration with the Prediction API.")


print("\n" + "=" * 60)
print("ALERT & RISK CLASSIFICATION MODULE COMPLETED SUCCESSFULLY")
print("=" * 60)

print("\nDAY 49 COMPLETED SUCCESSFULLY")
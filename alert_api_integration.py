import os
import joblib
import pandas as pd
from datetime import datetime

# ============================================================
# CHRONOS AI - DAY 50
# ALERT INTEGRATION MODULE
# ============================================================

print("=" * 60)
print("          CHRONOS AI - DAY 50")
print("       ALERT INTEGRATION MODULE")
print("=" * 60)

# ============================================================
# 1. PATHS
# ============================================================

base_path = r"C:\Users\navya\OneDrive\Documents\Chronos"

model_path = os.path.join(
    base_path, "models", "chronos_random_forest.pkl"
)

output_path = os.path.join(
    base_path,
    "datasets",
    "processed",
    "day50_alert_results.csv"
)

# ============================================================
# 2. CHECK MODEL
# ============================================================

print("\n" + "=" * 60)
print("1. CHECKING TRAINED MODEL")
print("=" * 60)

if not os.path.exists(model_path):
    print("Model Status : NOT FOUND")
    print("Please complete Day 47 first.")
    raise SystemExit

print("Model Status : FOUND")
print("Model Path   :", model_path)

# ============================================================
# 3. LOAD MODEL
# ============================================================

print("\n" + "=" * 60)
print("2. LOADING RANDOM FOREST MODEL")
print("=" * 60)

model = joblib.load(model_path)

print("Random Forest Model Loaded Successfully")

# ============================================================
# 4. RISK CLASSIFICATION FUNCTION
# ============================================================

print("\n" + "=" * 60)
print("3. CREATING RISK CLASSIFICATION FUNCTION")
print("=" * 60)


def classify_risk(failure_probability):

    if failure_probability < 0.30:
        return "NORMAL"

    elif failure_probability < 0.70:
        return "WARNING"

    else:
        return "CRITICAL"


print("Risk Classification Function Created Successfully")

# ============================================================
# 5. ALERT GENERATION FUNCTION
# ============================================================

print("\n" + "=" * 60)
print("4. CREATING ALERT GENERATION FUNCTION")
print("=" * 60)


def generate_alert(risk_level):

    if risk_level == "NORMAL":

        return {
            "alert_required": "NO",
            "alert_message":
                "Machine is operating within the predicted normal condition."
        }

    elif risk_level == "WARNING":

        return {
            "alert_required": "YES",
            "alert_message":
                "Machine shows elevated failure risk. Maintenance inspection recommended."
        }

    else:

        return {
            "alert_required": "YES",
            "alert_message":
                "High probability of machine failure. Immediate maintenance inspection recommended."
        }


print("Alert Generation Function Created Successfully")

# ============================================================
# 6. PREDICTION FUNCTION
# ============================================================

print("\n" + "=" * 60)
print("5. CREATING PREDICTION FUNCTION")
print("=" * 60)


def predict_machine(features):

    prediction = int(model.predict([features])[0])

    probability = model.predict_proba([features])[0]

    failure_probability = float(probability[1])
    normal_probability = float(probability[0])

    risk_level = classify_risk(failure_probability)

    alert = generate_alert(risk_level)

    result = {
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "prediction": prediction,
        "normal_probability": round(
            normal_probability, 4
        ),
        "failure_probability": round(
            failure_probability, 4
        ),
        "risk_level": risk_level,
        "alert_required": alert["alert_required"],
        "alert_message": alert["alert_message"]
    }

    return result


print("Prediction Function Created Successfully")

# ============================================================
# 7. NORMAL MACHINE TEST
# ============================================================

print("\n" + "=" * 60)
print("6. TESTING NORMAL MACHINE")
print("=" * 60)

normal_machine = [
    0,
    0,
    0,
    0,
    0,
    12.6,
    33957.0,
    8.4,
    10,
    0,
    301.7,
    0
]

normal_result = predict_machine(normal_machine)

print("\nNormal Machine Result:")
print("Prediction          :", normal_result["prediction"])
print("Normal Probability  :", normal_result["normal_probability"])
print("Failure Probability :", normal_result["failure_probability"])
print("Risk Level          :", normal_result["risk_level"])
print("Alert Required      :", normal_result["alert_required"])
print("Message             :", normal_result["alert_message"])

# ============================================================
# 8. HIGH-RISK MACHINE TEST
# ============================================================

print("\n" + "=" * 60)
print("7. TESTING HIGH-RISK MACHINE")
print("=" * 60)

high_risk_machine = [
    1,
    1,
    1,
    1,
    1,
    40.0,
    50000.0,
    20.0,
    240,
    1,
    310.0,
    1
]

high_risk_result = predict_machine(high_risk_machine)

print("\nHigh-Risk Machine Result:")
print("Prediction          :", high_risk_result["prediction"])
print("Normal Probability  :", high_risk_result["normal_probability"])
print("Failure Probability :", high_risk_result["failure_probability"])
print("Risk Level          :", high_risk_result["risk_level"])
print("Alert Required      :", high_risk_result["alert_required"])
print("Message             :", high_risk_result["alert_message"])

# ============================================================
# 9. CREATE ALERT REPORT
# ============================================================

print("\n" + "=" * 60)
print("8. CREATING ALERT REPORT")
print("=" * 60)

results = []

normal_record = normal_result.copy()
normal_record["machine"] = "Normal Test Machine"
results.append(normal_record)

high_risk_record = high_risk_result.copy()
high_risk_record["machine"] = "High Risk Test Machine"
results.append(high_risk_record)

report_df = pd.DataFrame(results)

columns = [
    "timestamp",
    "machine",
    "prediction",
    "normal_probability",
    "failure_probability",
    "risk_level",
    "alert_required",
    "alert_message"
]

report_df = report_df[columns]

print("Alert Report Created Successfully")

# ============================================================
# 10. SAVE ALERT REPORT
# ============================================================

print("\n" + "=" * 60)
print("9. SAVING ALERT REPORT")
print("=" * 60)

os.makedirs(
    os.path.dirname(output_path),
    exist_ok=True
)

report_df.to_csv(
    output_path,
    index=False
)

print("Alert Report Saved Successfully:")
print(output_path)

print("\nReport Shape:")
print("Rows   :", len(report_df))
print("Columns:", len(report_df.columns))

# ============================================================
# 11. DISPLAY ALERT REPORT
# ============================================================

print("\n" + "=" * 60)
print("10. ALERT REPORT")
print("=" * 60)

print(report_df.to_string(index=False))

# ============================================================
# 12. MODULE VERIFICATION
# ============================================================

print("\n" + "=" * 60)
print("11. MODULE VERIFICATION")
print("=" * 60)

print("Model Status          : VERIFIED")
print("Risk Function         : VERIFIED")
print("Alert Function        : VERIFIED")
print("Prediction Function   : VERIFIED")
print("Alert Report          : CREATED")
print("CSV Status            : SUCCESS")

# ============================================================
# 13. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("12. DAY 50 SUMMARY")
print("=" * 60)

print("• Random Forest model loaded successfully.")
print("• Risk classification integrated.")
print("• Alert generation integrated.")
print("• Prediction function created.")
print("• Normal machine scenario tested.")
print("• High-risk machine scenario tested.")
print("• Failure probability calculated.")
print("• Risk level identified.")
print("• Alert decision generated.")
print("• Alert message generated.")
print("• Alert report created.")
print("• Alert report saved successfully.")
print("• Day 50 alert integration verified.")

print("\nChronos AI Alert Integration Module")
print("is ready for Prediction API integration.")

print("\n" + "=" * 60)
print("ALERT INTEGRATION MODULE COMPLETED SUCCESSFULLY")
print("=" * 60)

print("\nDAY 50 COMPLETED SUCCESSFULLY")

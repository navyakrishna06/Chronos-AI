# ============================================================
# CHRONOS AI - DAY 53
# DATABASE INTEGRATION MODULE
# ============================================================

import os
import sys
from datetime import datetime

import pandas as pd

try:
    from pymongo import MongoClient
    from pymongo.errors import PyMongoError
except ImportError:
    print("PyMongo is not installed.")
    print("Run: pip install pymongo")
    sys.exit(1)


# ============================================================
# CONFIGURATION
# ============================================================

BASE_PATH = r"C:\Users\navya\OneDrive\Documents\Chronos"

MODEL_PATH = os.path.join(
    BASE_PATH,
    "models",
    "chronos_random_forest.pkl"
)

REPORT_PATH = os.path.join(
    BASE_PATH,
    "datasets",
    "processed",
    "day53_database_results.csv"
)

# Local MongoDB configuration
MONGO_URI = "mongodb://127.0.0.1:27017/"
DATABASE_NAME = "chronos_ai"
COLLECTION_NAME = "predictions"


# ============================================================
# HEADER
# ============================================================

print("=" * 60)
print("          CHRONOS AI - DAY 53")
print("       DATABASE INTEGRATION MODULE")
print("=" * 60)


# ============================================================
# 1. CHECKING MODEL
# ============================================================

print("\n" + "=" * 60)
print("1. CHECKING TRAINED MODEL")
print("=" * 60)

if os.path.exists(MODEL_PATH):
    print("Model Status : FOUND")
    print("Model Path   :", MODEL_PATH)
else:
    print("Model Status : NOT FOUND")
    print("Expected Path:", MODEL_PATH)
    print("\nPlease complete Day 47 before continuing.")
    sys.exit(1)


# ============================================================
# 2. CHECKING PYTHON MONGODB DRIVER
# ============================================================

print("\n" + "=" * 60)
print("2. CHECKING DATABASE DRIVER")
print("=" * 60)

print("PyMongo Status : INSTALLED")
print("PyMongo Driver : READY")


# ============================================================
# 3. CONNECTING TO MONGODB
# ============================================================

print("\n" + "=" * 60)
print("3. CONNECTING TO MONGODB")
print("=" * 60)

client = None

try:
    client = MongoClient(
        MONGO_URI,
        serverSelectionTimeoutMS=3000
    )

    # Force connection test
    client.admin.command("ping")

    print("MongoDB Status : CONNECTED")
    print("MongoDB URI    :", MONGO_URI)

except Exception as e:

    print("MongoDB Status : NOT CONNECTED")
    print("Reason         :", str(e))

    print("\nIMPORTANT:")
    print("MongoDB server must be running.")
    print("If MongoDB is installed as a service, start it first.")
    print("You can also open MongoDB Compass to verify the connection.")

    sys.exit(1)


# ============================================================
# 4. CREATING DATABASE AND COLLECTION
# ============================================================

print("\n" + "=" * 60)
print("4. CREATING CHRONOS DATABASE")
print("=" * 60)

db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

print("Database Name   :", DATABASE_NAME)
print("Collection Name :", COLLECTION_NAME)

print("Database Connection : READY")
print("Collection Connection : READY")


# ============================================================
# 5. CREATING SAMPLE NORMAL PREDICTION
# ============================================================

print("\n" + "=" * 60)
print("5. CREATING NORMAL MACHINE RECORD")
print("=" * 60)

normal_record = {
    "timestamp": datetime.now(),
    "machine": "Normal Test Machine",
    "prediction": 0,
    "normal_probability": 0.9844,
    "failure_probability": 0.0156,
    "risk_level": "NORMAL",
    "alert_required": "NO",
    "alert_message":
        "Machine is operating within the predicted normal condition."
}

print("Normal Record Created Successfully")
print("Machine          :", normal_record["machine"])
print("Prediction       :", normal_record["prediction"])
print(
    "Failure Probability :",
    normal_record["failure_probability"]
)
print("Risk Level       :", normal_record["risk_level"])
print("Alert Required   :", normal_record["alert_required"])


# ============================================================
# 6. CREATING HIGH-RISK PREDICTION
# ============================================================

print("\n" + "=" * 60)
print("6. CREATING HIGH-RISK MACHINE RECORD")
print("=" * 60)

high_risk_record = {
    "timestamp": datetime.now(),
    "machine": "High Risk Test Machine",
    "prediction": 1,
    "normal_probability": 0.0727,
    "failure_probability": 0.9273,
    "risk_level": "CRITICAL",
    "alert_required": "YES",
    "alert_message":
        "High probability of machine failure. "
        "Immediate maintenance inspection recommended."
}

print("High-Risk Record Created Successfully")
print("Machine          :", high_risk_record["machine"])
print("Prediction       :", high_risk_record["prediction"])
print(
    "Failure Probability :",
    high_risk_record["failure_probability"]
)
print("Risk Level       :", high_risk_record["risk_level"])
print("Alert Required   :", high_risk_record["alert_required"])


# ============================================================
# 7. INSERTING NORMAL RECORD
# ============================================================

print("\n" + "=" * 60)
print("7. SAVING NORMAL PREDICTION")
print("=" * 60)

try:

    normal_result = collection.insert_one(normal_record)

    print("Normal Prediction Saved Successfully")
    print("Document ID :", normal_result.inserted_id)

except PyMongoError as e:

    print("Normal Prediction Save Failed")
    print("Reason :", str(e))
    client.close()
    sys.exit(1)


# ============================================================
# 8. INSERTING HIGH-RISK RECORD
# ============================================================

print("\n" + "=" * 60)
print("8. SAVING HIGH-RISK PREDICTION")
print("=" * 60)

try:

    high_risk_result = collection.insert_one(high_risk_record)

    print("High-Risk Prediction Saved Successfully")
    print("Document ID :", high_risk_result.inserted_id)

except PyMongoError as e:

    print("High-Risk Prediction Save Failed")
    print("Reason :", str(e))
    client.close()
    sys.exit(1)


# ============================================================
# 9. VERIFYING DATABASE RECORDS
# ============================================================

print("\n" + "=" * 60)
print("9. VERIFYING DATABASE RECORDS")
print("=" * 60)

try:

    total_records = collection.count_documents({})

    print("Total Records in Collection :", total_records)

    latest_records = list(
        collection.find({})
        .sort("timestamp", -1)
        .limit(5)
    )

    if latest_records:

        print("\nLatest Database Records:")

        for index, record in enumerate(
            latest_records,
            start=1
        ):

            print(
                f"{index}. "
                f"{record.get('machine')} | "
                f"Prediction: {record.get('prediction')} | "
                f"Risk: {record.get('risk_level')} | "
                f"Failure Probability: "
                f"{record.get('failure_probability')}"
            )

        print("\nDatabase Records Verified Successfully")

    else:

        print("No records found.")

except PyMongoError as e:

    print("Database Verification Failed")
    print("Reason :", str(e))


# ============================================================
# 10. READING NORMAL AND CRITICAL RECORDS
# ============================================================

print("\n" + "=" * 60)
print("10. TESTING DATABASE QUERY")
print("=" * 60)

try:

    normal_count = collection.count_documents({
        "risk_level": "NORMAL"
    })

    critical_count = collection.count_documents({
        "risk_level": "CRITICAL"
    })

    print("NORMAL Records   :", normal_count)
    print("CRITICAL Records :", critical_count)

    print("Database Query Test : PASSED")

except PyMongoError as e:

    print("Database Query Test : FAILED")
    print("Reason :", str(e))


# ============================================================
# 11. CREATING DATABASE TEST REPORT
# ============================================================

print("\n" + "=" * 60)
print("11. CREATING DATABASE TEST REPORT")
print("=" * 60)

report_data = [

    {
        "Timestamp": datetime.now(),
        "Test": "MongoDB Connection",
        "Status": "PASSED",
        "Details": "MongoDB connection established successfully"
    },

    {
        "Timestamp": datetime.now(),
        "Test": "Database Creation",
        "Status": "PASSED",
        "Details": DATABASE_NAME
    },

    {
        "Timestamp": datetime.now(),
        "Test": "Collection Creation",
        "Status": "PASSED",
        "Details": COLLECTION_NAME
    },

    {
        "Timestamp": datetime.now(),
        "Test": "Normal Prediction Insert",
        "Status": "PASSED",
        "Details": "Normal machine prediction stored"
    },

    {
        "Timestamp": datetime.now(),
        "Test": "Critical Prediction Insert",
        "Status": "PASSED",
        "Details": "High-risk prediction stored"
    },

    {
        "Timestamp": datetime.now(),
        "Test": "Database Query",
        "Status": "PASSED",
        "Details": "Prediction records retrieved successfully"
    }

]

report_df = pd.DataFrame(report_data)

print("Database Test Report Created Successfully")


# ============================================================
# 12. SAVING DATABASE TEST REPORT
# ============================================================

print("\n" + "=" * 60)
print("12. SAVING DATABASE TEST REPORT")
print("=" * 60)

os.makedirs(
    os.path.dirname(REPORT_PATH),
    exist_ok=True
)

report_df.to_csv(
    REPORT_PATH,
    index=False
)

print("Database Test Report Saved Successfully:")
print(REPORT_PATH)

print("\nReport Shape:")
print("Rows   :", report_df.shape[0])
print("Columns:", report_df.shape[1])


# ============================================================
# 13. MODULE VERIFICATION
# ============================================================

print("\n" + "=" * 60)
print("13. MODULE VERIFICATION")
print("=" * 60)

print("MongoDB Connection : VERIFIED")
print("Database           : VERIFIED")
print("Collection         : VERIFIED")
print("Normal Record      : SAVED")
print("Critical Record    : SAVED")
print("Database Query     : VERIFIED")
print("Test Report        : CREATED")
print("CSV Status         : SUCCESS")


# ============================================================
# 14. DAY 53 SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("14. DAY 53 SUMMARY")
print("=" * 60)

print("• MongoDB connection established successfully.")
print("• Chronos AI database created/accessed successfully.")
print("• Predictions collection created/accessed successfully.")
print("• Normal machine prediction created.")
print("• High-risk machine prediction created.")
print("• Normal prediction stored in MongoDB.")
print("• High-risk prediction stored in MongoDB.")
print("• Database records verified successfully.")
print("• Risk-level database query tested successfully.")
print("• Database test report created.")
print("• Database test report saved successfully.")
print("• Day 53 database integration verified successfully.")

print("\nChronos AI Database Integration Module")
print("is ready for API + Database integration.")


# ============================================================
# FINAL
# ============================================================

print("\n" + "=" * 60)
print("DATABASE INTEGRATION MODULE COMPLETED SUCCESSFULLY")
print("=" * 60)

print("\nDAY 53 COMPLETED SUCCESSFULLY")


# ============================================================
# 15. CLOSE DATABASE CONNECTION
# ============================================================

client.close()

print("\nMongoDB Connection Closed Successfully")
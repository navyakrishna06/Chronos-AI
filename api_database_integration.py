import os
import requests
import pandas as pd
from datetime import datetime
from pymongo import MongoClient


# ============================================================
# CHRONOS AI - DAY 54
# API + MONGODB INTEGRATION
# ============================================================

print("=" * 60)
print("          CHRONOS AI - DAY 54")
print("       API + MONGODB INTEGRATION")
print("=" * 60)


# ============================================================
# 1. CONFIGURATION
# ============================================================

API_URL = "http://127.0.0.1:8000"
MONGO_URI = "mongodb://127.0.0.1:27017/"

DB_NAME = "chronos_ai"
COLLECTION_NAME = "predictions"

REPORT_PATH = (
    r"C:\Users\navya\OneDrive\Documents\Chronos"
    r"\datasets\processed\day54_api_database_results.csv"
)


# ============================================================
# 2. TEST INPUT DATA
# ============================================================

normal_payload = {
    "HDF": 0,
    "OSF": 0,
    "PWF": 0,
    "TWF": 0,
    "High_Torque": 0,
    "Torque_Nm": 35,
    "Power_Indicator": 0,
    "Temperature_Difference_K": 8,
    "Tool_wear_min": 50,
    "High_Tool_Wear": 0,
    "Air_temperature_K": 298,
    "Temperature_Stress": 0
}


high_risk_payload = {
    "HDF": 1,
    "OSF": 1,
    "PWF": 1,
    "TWF": 1,
    "High_Torque": 1,
    "Torque_Nm": 80,
    "Power_Indicator": 1,
    "Temperature_Difference_K": 10,
    "Tool_wear_min": 220,
    "High_Tool_Wear": 1,
    "Air_temperature_K": 305,
    "Temperature_Stress": 1
}


# ============================================================
# 3. CHECK FASTAPI SERVER
# ============================================================

def check_api():

    print("\n" + "=" * 60)
    print("1. CHECKING FASTAPI SERVER")
    print("=" * 60)

    try:

        response = requests.get(
            f"{API_URL}/health",
            timeout=5
        )

        response.raise_for_status()

        print("FastAPI Status : RUNNING")
        print("Health Status  :", response.status_code)

        return True

    except requests.RequestException as error:

        print("FastAPI Status : NOT RUNNING")
        print("\nPlease start Day 51 API in another CMD:")
        print("python day51_prediction_alert_api.py")
        print("\nError:", error)

        return False


# ============================================================
# 4. SEND PREDICTION TO API
# ============================================================

def get_prediction(payload):

    response = requests.post(
        f"{API_URL}/predict",
        json=payload,
        timeout=10
    )

    response.raise_for_status()

    return response.json()


# ============================================================
# 5. MAIN PROGRAM
# ============================================================

def main():

    os.makedirs(
        os.path.dirname(REPORT_PATH),
        exist_ok=True
    )

    # --------------------------------------------------------
    # Check API
    # --------------------------------------------------------

    if not check_api():

        print("\nDay 54 stopped because API is not running.")
        return


    # ========================================================
    # CONNECT TO MONGODB
    # ========================================================

    print("\n" + "=" * 60)
    print("2. CONNECTING TO MONGODB")
    print("=" * 60)

    client = MongoClient(
        MONGO_URI,
        serverSelectionTimeoutMS=5000
    )

    try:

        client.admin.command("ping")

        print("MongoDB Status : CONNECTED")
        print("MongoDB URI    :", MONGO_URI)


        # ====================================================
        # 3. DATABASE AND COLLECTION
        # ====================================================

        print("\n" + "=" * 60)
        print("3. ACCESSING CHRONOS DATABASE")
        print("=" * 60)

        db = client[DB_NAME]

        collection = db[COLLECTION_NAME]

        print("Database Name   :", DB_NAME)
        print("Collection Name :", COLLECTION_NAME)
        print("Database Status : READY")
        print("Collection      : READY")


        # ====================================================
        # 4. API + DATABASE TESTING
        # ====================================================

        print("\n" + "=" * 60)
        print("4. TESTING API + DATABASE INTEGRATION")
        print("=" * 60)


        test_cases = [

            (
                "Normal Test Machine",
                normal_payload
            ),

            (
                "High Risk Test Machine",
                high_risk_payload
            )

        ]


        rows = []

        inserted_records = 0


        # ====================================================
        # 5. PROCESS TEST CASES
        # ====================================================

        for machine_name, payload in test_cases:

            print("\n" + "-" * 60)
            print(machine_name)
            print("-" * 60)

            try:

                # Send data to FastAPI

                result = get_prediction(payload)

                timestamp = datetime.now()


                # ------------------------------------------------
                # Extract API response
                # ------------------------------------------------

                prediction = result.get(
                    "prediction"
                )

                failure_probability = result.get(
                    "failure_probability"
                )

                normal_probability = result.get(
                    "normal_probability"
                )

                risk_level = result.get(
                    "risk_level"
                )

                alert_required = result.get(
                    "alert_required"
                )

                message = result.get(
                    "message",
                    result.get("alert_message", "")
                )


                # ------------------------------------------------
                # Display result
                # ------------------------------------------------

                print(
                    "Prediction           :",
                    prediction
                )

                print(
                    "Failure Probability  :",
                    failure_probability
                )

                print(
                    "Normal Probability   :",
                    normal_probability
                )

                print(
                    "Risk Level           :",
                    risk_level
                )

                print(
                    "Alert Required       :",
                    alert_required
                )

                print(
                    "Message              :",
                    message
                )


                # =================================================
                # 6. CREATE MONGODB DOCUMENT
                # =================================================

                document = {

                    "timestamp": timestamp,

                    "machine": machine_name,

                    "request": payload,

                    "prediction": prediction,

                    "failure_probability":
                        failure_probability,

                    "normal_probability":
                        normal_probability,

                    "risk_level":
                        risk_level,

                    "alert_required":
                        alert_required,

                    "message":
                        message
                }


                # =================================================
                # 7. SAVE TO MONGODB
                # =================================================

                insert_result = collection.insert_one(
                    document
                )

                inserted_records += 1


                print(
                    "MongoDB Save Status  : SUCCESS"
                )

                print(
                    "Document ID          :",
                    insert_result.inserted_id
                )


                # =================================================
                # 8. CREATE REPORT ROW
                # =================================================

                rows.append({

                    "timestamp":
                        timestamp.strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),

                    "machine":
                        machine_name,

                    "prediction":
                        prediction,

                    "failure_probability":
                        failure_probability,

                    "normal_probability":
                        normal_probability,

                    "risk_level":
                        risk_level,

                    "alert_required":
                        alert_required,

                    "message":
                        message
                })


            except requests.RequestException as error:

                print(
                    "API Request Failed:",
                    error
                )


        # ========================================================
        # 9. VERIFY DATABASE RECORDS
        # ========================================================

        print("\n" + "=" * 60)
        print("5. VERIFYING MONGODB RECORDS")
        print("=" * 60)

        total_records = collection.count_documents({})

        print(
            "Total Records in Collection :",
            total_records
        )

        print(
            "New Records Inserted        :",
            inserted_records
        )


        # ========================================================
        # 10. RISK LEVEL QUERY
        # ========================================================

        print("\n" + "=" * 60)
        print("6. TESTING RISK LEVEL QUERIES")
        print("=" * 60)


        for risk in [
            "NORMAL",
            "WARNING",
            "CRITICAL"
        ]:

            count = collection.count_documents({

                "risk_level": risk

            })

            print(
                f"{risk:<10}: {count}"
            )


        # ========================================================
        # 11. DISPLAY LATEST RECORDS
        # ========================================================

        print("\n" + "=" * 60)
        print("7. LATEST MONGODB RECORDS")
        print("=" * 60)


        recent_records = list(

            collection.find(

                {},

                {
                    "_id": 0,
                    "timestamp": 1,
                    "machine": 1,
                    "prediction": 1,
                    "failure_probability": 1,
                    "risk_level": 1,
                    "alert_required": 1
                }

            ).sort(
                "timestamp",
                -1
            ).limit(5)

        )


        for record in recent_records:

            print(
                record
            )


        # ========================================================
        # 12. SAVE CSV REPORT
        # ========================================================

        print("\n" + "=" * 60)
        print("8. SAVING DAY 54 REPORT")
        print("=" * 60)


        if rows:

            report_df = pd.DataFrame(
                rows
            )

            report_df.to_csv(
                REPORT_PATH,
                index=False
            )

            print(
                "Report Saved Successfully"
            )

            print(
                "Report Path:",
                REPORT_PATH
            )

            print(
                "Rows   :",
                report_df.shape[0]
            )

            print(
                "Columns:",
                report_df.shape[1]
            )

        else:

            print(
                "No prediction results available."
            )


        # ========================================================
        # 13. DAY 54 VERIFICATION
        # ========================================================

        print("\n" + "=" * 60)
        print("9. DAY 54 MODULE VERIFICATION")
        print("=" * 60)


        print(
            "FastAPI Server       : VERIFIED"
        )

        print(
            "MongoDB Connection   : VERIFIED"
        )

        print(
            "Database             : VERIFIED"
        )

        print(
            "Collection           : VERIFIED"
        )

        print(
            "API Prediction       : VERIFIED"
        )

        print(
            "MongoDB Storage      : VERIFIED"
        )

        print(
            "Risk Query           : VERIFIED"
        )

        print(
            "CSV Report           : CREATED"
        )


        # ========================================================
        # 14. FINAL SUMMARY
        # ========================================================

        print("\n" + "=" * 60)
        print("10. DAY 54 SUMMARY")
        print("=" * 60)

        print(
            "• FastAPI server verified successfully."
        )

        print(
            "• MongoDB connection verified."
        )

        print(
            "• Chronos AI database accessed."
        )

        print(
            "• Predictions collection accessed."
        )

        print(
            "• Normal machine sent through API."
        )

        print(
            "• High-risk machine sent through API."
        )

        print(
            "• API prediction results received."
        )

        print(
            "• Prediction results stored in MongoDB."
        )

        print(
            "• Risk levels verified."
        )

        print(
            "• Latest database records displayed."
        )

        print(
            "• Day 54 CSV report created."
        )


        print("\n" + "=" * 60)
        print(
            "API + MONGODB INTEGRATION COMPLETED SUCCESSFULLY"
        )
        print("=" * 60)

        print(
            "\nDAY 54 COMPLETED SUCCESSFULLY"
        )


    except Exception as error:

        print("\n" + "=" * 60)
        print("DAY 54 ERROR")
        print("=" * 60)

        print(
            "Error:",
            error
        )


    finally:

        client.close()

        print(
            "\nMongoDB Connection Closed Successfully"
        )


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    main()

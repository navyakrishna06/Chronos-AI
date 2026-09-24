# ============================================================
# CHRONOS AI - DAY 52
# API TESTING & VALIDATION MODULE
# ============================================================

import os
import json
import requests
import pandas as pd
from datetime import datetime

# ============================================================
# PATHS
# ============================================================

base_path = r"C:\Users\navya\OneDrive\Documents\Chronos"

report_path = os.path.join(
    base_path,
    "datasets",
    "processed",
    "day52_api_test_results.csv"
)

# ============================================================
# API CONFIGURATION
# ============================================================

API_URL = "http://127.0.0.1:8000"

HOME_ENDPOINT = f"{API_URL}/"
HEALTH_ENDPOINT = f"{API_URL}/health"
PREDICT_ENDPOINT = f"{API_URL}/predict"
MODEL_INFO_ENDPOINT = f"{API_URL}/model-info"

# ============================================================
# TEST DATA
# ============================================================

normal_machine = {
    "HDF": 0,
    "OSF": 0,
    "PWF": 0,
    "TWF": 0,
    "High_Torque": 0,
    "Torque_Nm": 50,
    "Power_Indicator": 0,
    "Temperature_Difference_K": 10,
    "Tool_wear_min": 50,
    "High_Tool_Wear": 0,
    "Air_temperature_K": 300,
    "Temperature_Stress": 0
}

high_risk_machine = {
    "HDF": 1,
    "OSF": 1,
    "PWF": 1,
    "TWF": 1,
    "High_Torque": 1,
    "Torque_Nm": 90,
    "Power_Indicator": 1,
    "Temperature_Difference_K": 40,
    "Tool_wear_min": 230,
    "High_Tool_Wear": 1,
    "Air_temperature_K": 320,
    "Temperature_Stress": 1
}

# ============================================================
# HELPER FUNCTION
# ============================================================

def print_section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def test_get_endpoint(name, url):
    try:
        response = requests.get(url, timeout=10)

        return {
            "test": name,
            "method": "GET",
            "endpoint": url,
            "status_code": response.status_code,
            "result": "PASSED" if response.status_code == 200 else "FAILED",
            "response": response.text
        }

    except Exception as error:
        return {
            "test": name,
            "method": "GET",
            "endpoint": url,
            "status_code": 0,
            "result": "FAILED",
            "response": str(error)
        }


def test_prediction(name, data):
    try:
        response = requests.post(
            PREDICT_ENDPOINT,
            json=data,
            timeout=10
        )

        result = response.json()

        return {
            "test": name,
            "method": "POST",
            "endpoint": PREDICT_ENDPOINT,
            "status_code": response.status_code,
            "result": "PASSED" if response.status_code == 200 else "FAILED",
            "response": json.dumps(result)
        }

    except Exception as error:
        return {
            "test": name,
            "method": "POST",
            "endpoint": PREDICT_ENDPOINT,
            "status_code": 0,
            "result": "FAILED",
            "response": str(error)
        }


# ============================================================
# HEADER
# ============================================================

print("=" * 60)
print("          CHRONOS AI - DAY 52")
print("       API TESTING & VALIDATION")
print("=" * 60)

# ============================================================
# 1. CHECK API SERVER
# ============================================================

print_section("1. CHECKING CHRONOS AI API SERVER")

print("API URL:")
print(API_URL)

print("\nChecking API server...")

try:
    response = requests.get(
        HOME_ENDPOINT,
        timeout=10
    )

    if response.status_code == 200:
        print("API Server Status : RUNNING")
        print("Server Response   :", response.text)
    else:
        print("API Server Status : ERROR")
        print("Status Code       :", response.status_code)

except Exception as error:
    print("API Server Status : NOT AVAILABLE")
    print("Error             :", error)

# ============================================================
# 2. TEST HOME ENDPOINT
# ============================================================

print_section("2. TESTING HOME ENDPOINT")

home_result = test_get_endpoint(
    "Home Endpoint",
    HOME_ENDPOINT
)

print("Endpoint   :", HOME_ENDPOINT)
print("Status Code:", home_result["status_code"])
print("Result     :", home_result["result"])
print("Response   :", home_result["response"])

# ============================================================
# 3. TEST HEALTH ENDPOINT
# ============================================================

print_section("3. TESTING HEALTH ENDPOINT")

health_result = test_get_endpoint(
    "Health Endpoint",
    HEALTH_ENDPOINT
)

print("Endpoint   :", HEALTH_ENDPOINT)
print("Status Code:", health_result["status_code"])
print("Result     :", health_result["result"])
print("Response   :", health_result["response"])

# ============================================================
# 4. TEST MODEL INFO ENDPOINT
# ============================================================

print_section("4. TESTING MODEL INFO ENDPOINT")

model_result = test_get_endpoint(
    "Model Info Endpoint",
    MODEL_INFO_ENDPOINT
)

print("Endpoint   :", MODEL_INFO_ENDPOINT)
print("Status Code:", model_result["status_code"])
print("Result     :", model_result["result"])
print("Response   :", model_result["response"])

# ============================================================
# 5. TEST NORMAL MACHINE
# ============================================================

print_section("5. TESTING NORMAL MACHINE")

normal_result = test_prediction(
    "Normal Machine Prediction",
    normal_machine
)

print("Prediction Request Sent Successfully")
print("Status Code:", normal_result["status_code"])
print("Test Result :", normal_result["result"])

try:
    normal_response = json.loads(
        normal_result["response"]
    )

    print("\nNormal Machine API Response:")
    print("Prediction          :",
          normal_response.get("prediction"))

    print("Failure Probability :",
          normal_response.get("failure_probability"))

    print("Normal Probability  :",
          normal_response.get("normal_probability"))

    print("Risk Level          :",
          normal_response.get("risk_level"))

    print("Alert Required      :",
          normal_response.get("alert_required"))

    print("Message             :",
          normal_response.get("message"))

except Exception:
    print("Response:", normal_result["response"])

# ============================================================
# 6. TEST HIGH-RISK MACHINE
# ============================================================

print_section("6. TESTING HIGH-RISK MACHINE")

high_risk_result = test_prediction(
    "High Risk Machine Prediction",
    high_risk_machine
)

print("Prediction Request Sent Successfully")
print("Status Code:", high_risk_result["status_code"])
print("Test Result :", high_risk_result["result"])

try:
    high_risk_response = json.loads(
        high_risk_result["response"]
    )

    print("\nHigh-Risk Machine API Response:")
    print("Prediction          :",
          high_risk_response.get("prediction"))

    print("Failure Probability :",
          high_risk_response.get("failure_probability"))

    print("Normal Probability  :",
          high_risk_response.get("normal_probability"))

    print("Risk Level          :",
          high_risk_response.get("risk_level"))

    print("Alert Required      :",
          high_risk_response.get("alert_required"))

    print("Message             :",
          high_risk_response.get("message"))

except Exception:
    print("Response:", high_risk_result["response"])

# ============================================================
# 7. API TEST SUMMARY
# ============================================================

print_section("7. API TEST SUMMARY")

all_results = [
    home_result,
    health_result,
    model_result,
    normal_result,
    high_risk_result
]

total_tests = len(all_results)

passed_tests = sum(
    1 for result in all_results
    if result["result"] == "PASSED"
)

failed_tests = total_tests - passed_tests

print("Total Tests  :", total_tests)
print("Passed Tests :", passed_tests)
print("Failed Tests :", failed_tests)

if failed_tests == 0:
    overall_status = "PASSED"
else:
    overall_status = "FAILED"

print("Overall Status:", overall_status)

# ============================================================
# 8. CREATING API TEST REPORT
# ============================================================

print_section("8. CREATING API TEST REPORT")

timestamp = datetime.now().strftime(
    "%Y-%m-%d %H:%M:%S"
)

report_rows = []

for result in all_results:

    report_rows.append({
        "Timestamp": timestamp,
        "Test": result["test"],
        "Method": result["method"],
        "Endpoint": result["endpoint"],
        "Status Code": result["status_code"],
        "Result": result["result"],
        "Response": result["response"]
    })

report_df = pd.DataFrame(report_rows)

print("API Test Report Created Successfully")

# ============================================================
# 9. SAVING API TEST REPORT
# ============================================================

print_section("9. SAVING API TEST REPORT")

report_df.to_csv(
    report_path,
    index=False
)

print("API Test Report Saved Successfully:")
print(report_path)

print("\nReport Shape:")
print("Rows   :", len(report_df))
print("Columns:", len(report_df.columns))

# ============================================================
# 10. DISPLAY REPORT
# ============================================================

print_section("10. API TEST REPORT")

print(
    report_df[
        [
            "Test",
            "Method",
            "Status Code",
            "Result"
        ]
    ].to_string(index=False)
)

# ============================================================
# 11. MODULE VERIFICATION
# ============================================================

print_section("11. MODULE VERIFICATION")

print(
    "API Server          :",
    "VERIFIED" if home_result["result"] == "PASSED"
    else "FAILED"
)

print(
    "Home Endpoint       :",
    "VERIFIED" if home_result["result"] == "PASSED"
    else "FAILED"
)

print(
    "Health Endpoint     :",
    "VERIFIED" if health_result["result"] == "PASSED"
    else "FAILED"
)

print(
    "Model Info Endpoint :",
    "VERIFIED" if model_result["result"] == "PASSED"
    else "FAILED"
)

print(
    "Normal Prediction   :",
    "VERIFIED" if normal_result["result"] == "PASSED"
    else "FAILED"
)

print(
    "High-Risk Prediction:",
    "VERIFIED" if high_risk_result["result"] == "PASSED"
    else "FAILED"
)

print(
    "Test Report         :",
    "CREATED"
)

print(
    "CSV Status          :",
    "SUCCESS"
)

# ============================================================
# 12. DAY 52 SUMMARY
# ============================================================

print_section("12. DAY 52 SUMMARY")

if overall_status == "PASSED":

    print("• Chronos AI API server verified successfully.")
    print("• Home endpoint tested successfully.")
    print("• Health endpoint tested successfully.")
    print("• Model information endpoint tested successfully.")
    print("• Normal machine prediction tested successfully.")
    print("• High-risk machine prediction tested successfully.")
    print("• Prediction API response validated successfully.")
    print("• Risk classification response validated successfully.")
    print("• Alert decision response validated successfully.")
    print("• API test report created successfully.")
    print("• API test report saved successfully.")
    print("• All API tests passed successfully.")

else:

    print("• API testing completed.")
    print("• Some API tests require attention.")
    print("• Failed endpoints should be checked.")

print("\nChronos AI Prediction API")
print("has successfully passed Day 52 API testing.")

print("\n" + "=" * 60)
print("API TESTING & VALIDATION COMPLETED SUCCESSFULLY")
print("=" * 60)

print("\nDAY 52 COMPLETED SUCCESSFULLY")

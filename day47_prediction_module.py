# ============================================================
# CHRONOS AI - DAY 47
# ML PREDICTION MODULE
# ============================================================

import os
import joblib

import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)


# ============================================================
# PATHS
# ============================================================

base_path = r"C:\Users\navya\OneDrive\Documents\Chronos"

train_path = os.path.join(
    base_path,
    "datasets",
    "processed",
    "ml_train.csv"
)

test_path = os.path.join(
    base_path,
    "datasets",
    "processed",
    "ml_test.csv"
)

models_path = os.path.join(
    base_path,
    "models"
)

model_path = os.path.join(
    models_path,
    "chronos_random_forest.pkl"
)

metadata_path = os.path.join(
    models_path,
    "chronos_prediction_metadata.joblib"
)

os.makedirs(models_path, exist_ok=True)


# ============================================================
# HEADER
# ============================================================

print("=" * 60)
print("          CHRONOS AI - DAY 47")
print("          ML PREDICTION MODULE")
print("=" * 60)


# ============================================================
# 1. CHECK DATASET FILES
# ============================================================

print("\n" + "=" * 60)
print("1. CHECKING DATASET FILES")
print("=" * 60)

if not os.path.exists(train_path):
    print("Training dataset not found:")
    print(train_path)
    raise FileNotFoundError(train_path)

if not os.path.exists(test_path):
    print("Testing dataset not found:")
    print(test_path)
    raise FileNotFoundError(test_path)

print("Training Dataset : FOUND")
print("Testing Dataset  : FOUND")


# ============================================================
# 2. LOAD DATASETS
# ============================================================

print("\n" + "=" * 60)
print("2. LOADING ML DATASETS")
print("=" * 60)

train_df = pd.read_csv(train_path)

test_df = pd.read_csv(test_path)

print("Training Dataset Loaded Successfully")
print("Testing Dataset Loaded Successfully")

print("\nTraining Shape:", train_df.shape)
print("Testing Shape :", test_df.shape)


# ============================================================
# 3. DEFINE TARGET AND FEATURES
# ============================================================

print("\n" + "=" * 60)
print("3. TARGET AND FEATURE IDENTIFICATION")
print("=" * 60)

target = "Machine failure"

feature_columns = [
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

print("\nTarget Variable:")
print("-", target)

print("\nInput Features:")

for feature in feature_columns:
    print("-", feature)

print("\nTotal Features:", len(feature_columns))


# ============================================================
# 4. CHECK REQUIRED COLUMNS
# ============================================================

print("\n" + "=" * 60)
print("4. VALIDATING DATASET COLUMNS")
print("=" * 60)

required_columns = feature_columns + [target]

missing_train_columns = [
    column
    for column in required_columns
    if column not in train_df.columns
]

missing_test_columns = [
    column
    for column in required_columns
    if column not in test_df.columns
]

if missing_train_columns:
    print("Missing columns in training dataset:")
    print(missing_train_columns)
    raise ValueError("Training dataset columns are incomplete.")

if missing_test_columns:
    print("Missing columns in testing dataset:")
    print(missing_test_columns)
    raise ValueError("Testing dataset columns are incomplete.")

print("Training Dataset Columns : VALID")
print("Testing Dataset Columns  : VALID")


# ============================================================
# 5. SEPARATE FEATURES AND TARGET
# ============================================================

print("\n" + "=" * 60)
print("5. SEPARATING FEATURES AND TARGET")
print("=" * 60)

X_train = train_df[feature_columns]

y_train = train_df[target]

X_test = test_df[feature_columns]

y_test = test_df[target]

print("Training Features Shape:", X_train.shape)
print("Training Target Shape  :", y_train.shape)

print("Testing Features Shape :", X_test.shape)
print("Testing Target Shape   :", y_test.shape)

print("\nFeatures and target separated successfully.")


# ============================================================
# 6. CHECK TARGET DISTRIBUTION
# ============================================================

print("\n" + "=" * 60)
print("6. MACHINE FAILURE DISTRIBUTION")
print("=" * 60)

print("\nTraining Target Distribution:")

print(
    y_train.value_counts()
    .sort_index()
)

print("\nTesting Target Distribution:")

print(
    y_test.value_counts()
    .sort_index()
)


# ============================================================
# 7. TRAIN RANDOM FOREST
# ============================================================

print("\n" + "=" * 60)
print("7. TRAINING RANDOM FOREST MODEL")
print("=" * 60)

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=8,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)

print("Random Forest Configuration:")
print("- Number of Trees : 100")
print("- Maximum Depth   : 8")
print("- Random Seed     : 42")
print("- Class Weight    : balanced")

print("\nTraining model...")

model.fit(
    X_train,
    y_train
)

print("Random Forest Model Trained Successfully")


# ============================================================
# 8. GENERATE PREDICTIONS
# ============================================================

print("\n" + "=" * 60)
print("8. GENERATING PREDICTIONS")
print("=" * 60)

predictions = model.predict(X_test)

probabilities = model.predict_proba(X_test)

failure_probability = probabilities[:, 1]

print("Predictions Generated Successfully")


# ============================================================
# 9. SAMPLE PREDICTIONS
# ============================================================

print("\n" + "=" * 60)
print("9. SAMPLE PREDICTIONS")
print("=" * 60)

sample_predictions = pd.DataFrame({

    "Actual Failure": y_test.values[:10],

    "Predicted Failure": predictions[:10],

    "Failure Probability": failure_probability[:10]

})

sample_predictions["Failure Probability"] = (
    sample_predictions["Failure Probability"]
    .round(4)
)

print(sample_predictions.to_string(index=False))


# ============================================================
# 10. MODEL EVALUATION
# ============================================================

print("\n" + "=" * 60)
print("10. MODEL EVALUATION")
print("=" * 60)

accuracy = accuracy_score(
    y_test,
    predictions
)

precision = precision_score(
    y_test,
    predictions,
    zero_division=0
)

recall = recall_score(
    y_test,
    predictions,
    zero_division=0
)

f1 = f1_score(
    y_test,
    predictions,
    zero_division=0
)

auc = roc_auc_score(
    y_test,
    failure_probability
)

print("Accuracy  :", round(accuracy, 4))
print("Precision :", round(precision, 4))
print("Recall    :", round(recall, 4))
print("F1 Score  :", round(f1, 4))
print("ROC-AUC   :", round(auc, 4))


# ============================================================
# 11. CONFUSION MATRIX VALUES
# ============================================================

print("\n" + "=" * 60)
print("11. CONFUSION MATRIX")
print("=" * 60)

tn = ((y_test == 0) & (predictions == 0)).sum()
fp = ((y_test == 0) & (predictions == 1)).sum()
fn = ((y_test == 1) & (predictions == 0)).sum()
tp = ((y_test == 1) & (predictions == 1)).sum()

print("True Negative  :", tn)
print("False Positive :", fp)
print("False Negative :", fn)
print("True Positive  :", tp)


# ============================================================
# 12. FEATURE IMPORTANCE
# ============================================================

print("\n" + "=" * 60)
print("12. FEATURE IMPORTANCE")
print("=" * 60)

feature_importance = pd.DataFrame({

    "Feature": feature_columns,

    "Importance": model.feature_importances_

})

feature_importance = (
    feature_importance
    .sort_values(
        by="Importance",
        ascending=False
    )
    .reset_index(drop=True)
)

print("\nFeature Importance Ranking:")

for index, row in feature_importance.iterrows():

    print(
        f"{index + 1}. "
        f"{row['Feature']} -> "
        f"{row['Importance']:.6f}"
    )


# ============================================================
# 13. SAVE PREDICTION MODEL
# ============================================================

print("\n" + "=" * 60)
print("13. SAVING PREDICTION MODEL")
print("=" * 60)

joblib.dump(
    model,
    model_path
)

print("Prediction Model Saved Successfully:")
print(model_path)


# ============================================================
# 14. CREATE MODEL METADATA
# ============================================================

print("\n" + "=" * 60)
print("14. SAVING MODEL METADATA")
print("=" * 60)

metadata = {

    "project": "Chronos AI",

    "module": "ML Prediction Module",

    "model_name": "Chronos Random Forest",

    "algorithm": "Random Forest Classifier",

    "n_estimators": 100,

    "max_depth": 8,

    "random_state": 42,

    "class_weight": "balanced",

    "target_variable": target,

    "features": feature_columns,

    "training_rows": int(len(train_df)),

    "testing_rows": int(len(test_df)),

    "accuracy": float(accuracy),

    "precision": float(precision),

    "recall": float(recall),

    "f1_score": float(f1),

    "roc_auc": float(auc),

    "true_negative": int(tn),

    "false_positive": int(fp),

    "false_negative": int(fn),

    "true_positive": int(tp),

    "feature_importance": {
        row["Feature"]: float(row["Importance"])
        for _, row in feature_importance.iterrows()
    }

}

joblib.dump(
    metadata,
    metadata_path
)

print("Prediction Metadata Saved Successfully:")
print(metadata_path)


# ============================================================
# 15. VERIFY SAVED MODEL
# ============================================================

print("\n" + "=" * 60)
print("15. MODEL VERIFICATION")
print("=" * 60)

if not os.path.exists(model_path):

    print("Model Verification FAILED")

else:

    loaded_model = joblib.load(
        model_path
    )

    print("Model File Status : CREATED SUCCESSFULLY")

    print(
        "Model Type        :",
        type(loaded_model).__name__
    )

    print(
        "Number of Trees   :",
        loaded_model.n_estimators
    )

    print(
        "Maximum Depth     :",
        loaded_model.max_depth
    )


# ============================================================
# 16. TEST SAVED MODEL
# ============================================================

print("\n" + "=" * 60)
print("16. TESTING SAVED MODEL")
print("=" * 60)

test_sample = X_test.iloc[[0]]

loaded_prediction = loaded_model.predict(
    test_sample
)

loaded_probability = loaded_model.predict_proba(
    test_sample
)[0][1]

print("Sample Prediction :", int(loaded_prediction[0]))

print(
    "Failure Probability :",
    round(float(loaded_probability), 4)
)

if loaded_prediction[0] == 1:

    print("Prediction Result : MACHINE FAILURE")

else:

    print("Prediction Result : NORMAL")


# ============================================================
# 17. PREDICTION FUNCTION
# ============================================================

print("\n" + "=" * 60)
print("17. PREDICTION FUNCTION")
print("=" * 60)


def predict_machine_failure(input_data):

    """
    Predict machine failure from input feature values.

    input_data must be a dictionary containing
    all required feature names.
    """

    input_df = pd.DataFrame(
        [input_data]
    )

    input_df = input_df[
        feature_columns
    ]

    prediction = loaded_model.predict(
        input_df
    )[0]

    probability = loaded_model.predict_proba(
        input_df
    )[0][1]

    if prediction == 1:

        result = "MACHINE FAILURE"

    else:

        result = "NORMAL"

    return {

        "prediction": int(prediction),

        "failure_probability": round(
            float(probability),
            4
        ),

        "result": result

    }


# ============================================================
# 18. TEST PREDICTION FUNCTION
# ============================================================

print("\n" + "=" * 60)
print("18. TESTING PREDICTION FUNCTION")
print("=" * 60)

sample_input = X_test.iloc[0].to_dict()

result = predict_machine_failure(
    sample_input
)

print("Prediction Function Result:")

print("Prediction           :", result["prediction"])

print(
    "Failure Probability  :",
    result["failure_probability"]
)

print(
    "Final Result         :",
    result["result"]
)


# ============================================================
# 19. SAVE SAMPLE PREDICTIONS
# ============================================================

print("\n" + "=" * 60)
print("19. SAVING SAMPLE PREDICTIONS")
print("=" * 60)

prediction_output_path = os.path.join(
    base_path,
    "datasets",
    "processed",
    "day47_predictions.csv"
)

prediction_results = pd.DataFrame({

    "Actual Failure": y_test,

    "Predicted Failure": predictions,

    "Failure Probability": failure_probability

})

prediction_results.to_csv(
    prediction_output_path,
    index=False
)

print("Prediction Results Saved Successfully:")
print(prediction_output_path)


# ============================================================
# 20. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("20. DAY 47 SUMMARY")
print("=" * 60)

print("• ML training dataset loaded successfully.")
print("• ML testing dataset loaded successfully.")
print("• Target variable identified successfully.")
print("• Input features validated successfully.")
print("• Random Forest model trained successfully.")
print("• Test predictions generated successfully.")
print("• Failure probabilities calculated successfully.")
print("• Accuracy calculated successfully.")
print("• Precision calculated successfully.")
print("• Recall calculated successfully.")
print("• F1 Score calculated successfully.")
print("• ROC-AUC calculated successfully.")
print("• Confusion matrix generated successfully.")
print("• Feature importance calculated successfully.")
print("• Prediction model saved successfully.")
print("• Model metadata saved successfully.")
print("• Saved model verified successfully.")
print("• Prediction function created successfully.")
print("• Sample prediction tested successfully.")
print("• Prediction results saved successfully.")

print("\nChronos AI prediction module is ready for API integration.")


# ============================================================
# COMPLETION
# ============================================================

print("\n" + "=" * 60)
print("ML PREDICTION MODULE COMPLETED SUCCESSFULLY")
print("=" * 60)

print("\nDAY 47 COMPLETED SUCCESSFULLY")
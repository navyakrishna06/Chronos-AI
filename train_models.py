import pandas as pd
import joblib
import os

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


# Paths
data_path = "datasets/ml_ready"

model_path = "models"

# Load training data
print("Loading ML datasets...")

X_train = pd.read_csv(f"{data_path}/X_train.csv")
X_test = pd.read_csv(f"{data_path}/X_test.csv")

y_train = pd.read_csv(f"{data_path}/y_train.csv").values.ravel()
y_test = pd.read_csv(f"{data_path}/y_test.csv").values.ravel()


print("Training Shape:", X_train.shape)
print("Testing Shape:", X_test.shape)


# Models

models = {

    "Logistic Regression": LogisticRegression(
        max_iter=1000
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        random_state=42
    ),

    "XGBoost": XGBClassifier(
        n_estimators=100,
        random_state=42
    )
}


results = {}


# Training

for name, model in models.items():

    print("\nTraining:", name)

    model.fit(
        X_train,
        y_train
    )

    prediction = model.predict(
        X_test
    )


    accuracy = accuracy_score(
        y_test,
        prediction
    )

    precision = precision_score(
        y_test,
        prediction,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        prediction,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        prediction,
        zero_division=0
    )


    results[name] = {
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1
    }


    print("Accuracy:", accuracy)
    print("F1 Score:", f1)


    # Save model

    filename = name.replace(" ", "_") + ".pkl"

    joblib.dump(
        model,
        f"{model_path}/{filename}"
    )


# Display comparison

print("\nModel Comparison")

for model, score in results.items():
    print("\n", model)
    print(score)


# Select best model based on F1

best_model_name = max(
    results,
    key=lambda x: results[x]["F1 Score"]
)


best_model = models[best_model_name]


joblib.dump(
    best_model,
    f"{model_path}/chronos_best_model.pkl"
)


print("\nBest Model:", best_model_name)
print("Saved as chronos_best_model.pkl")
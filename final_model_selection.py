import pandas as pd

# Final Model Comparison
results = {
    "Algorithm": [
        "Logistic Regression",
        "Decision Tree",
        "Random Forest",
        "SVM",
        "KNN",
        "Optimized Random Forest"
    ],

    "Accuracy (%)": [
        97.25,
        97.80,
        98.40,
        97.00,
        97.05,
        98.25
    ]
}

df = pd.DataFrame(results)

print("\n========== FINAL MODEL COMPARISON ==========\n")
print(df)

best = df.loc[df["Accuracy (%)"].idxmax()]

print("\n====================================")
print("Final Selected Model")
print("====================================")

print(f"Algorithm : {best['Algorithm']}")
print(f"Accuracy  : {best['Accuracy (%)']}%")

print("\nReason:")
print("- Highest Accuracy")
print("- Better Prediction Performance")
print("- Less Overfitting")
print("- Suitable for Predictive Maintenance")
print("- Selected as Final Model for Chronos AI")
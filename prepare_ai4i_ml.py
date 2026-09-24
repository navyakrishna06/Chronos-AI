import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os

# Paths
input_file = "datasets/processed/ai4i_clean.csv"

output_dir = "datasets/ml_ready"

os.makedirs(output_dir, exist_ok=True)

print("Loading cleaned dataset...")

df = pd.read_csv(input_file)

print("Original Shape:", df.shape)


# -----------------------------
# 1. Separate Features & Target
# -----------------------------

X = df.drop("Machine failure", axis=1)
y = df["Machine failure"]


# -----------------------------
# 2. Encode categorical column
# -----------------------------

encoder = LabelEncoder()

X["Type"] = encoder.fit_transform(X["Type"])

print("\nAfter Encoding:")
print(X.head())


# -----------------------------
# 3. Feature Scaling
# -----------------------------

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

X_scaled = pd.DataFrame(
    X_scaled,
    columns=X.columns
)


# -----------------------------
# 4. Train Test Split
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


print("\nTraining Data:", X_train.shape)
print("Testing Data:", X_test.shape)


# -----------------------------
# 5. Save ML datasets
# -----------------------------

X_train.to_csv(
    output_dir + "/X_train.csv",
    index=False
)

X_test.to_csv(
    output_dir + "/X_test.csv",
    index=False
)

y_train.to_csv(
    output_dir + "/y_train.csv",
    index=False
)

y_test.to_csv(
    output_dir + "/y_test.csv",
    index=False
)


# Save preprocessing objects

joblib.dump(
    encoder,
    output_dir + "/type_encoder.pkl"
)

joblib.dump(
    scaler,
    output_dir + "/scaler.pkl"
)


print("\nML Data Preparation Completed!")
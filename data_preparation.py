import pandas as pd
from sklearn.model_selection import train_test_split

# Load cleaned dataset
df = pd.read_csv("datasets/processed/ai4i_clean.csv")

# Encode Type column
df["Type"] = df["Type"].map({"L":0,"M":1,"H":2})

# Select features
X = df[
[
"Type",
"Air temperature [K]",
"Process temperature [K]",
"Rotational speed [rpm]",
"Torque [Nm]",
"Tool wear [min]"
]
]

# Target
Y = df["Machine failure"]

# Split dataset
X_train, X_test, Y_train, Y_test = train_test_split(
X,
Y,
test_size=0.2,
random_state=42
)

print("Training Data:", X_train.shape)
print("Testing Data:", X_test.shape)

print("\nTarget Train:", Y_train.shape)
print("Target Test:", Y_test.shape)
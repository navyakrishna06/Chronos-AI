# ==========================================
# CHRONOS AI
# Day 42 - Feature Relationship Analysis
# ==========================================

import os
import matplotlib.pyplot as plt

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, corr

print("=" * 60)
print("          CHRONOS AI - DAY 42")
print("      FEATURE RELATIONSHIP ANALYSIS")
print("=" * 60)

# ------------------------------------------------
# Python Configuration
# ------------------------------------------------

python_path = r"C:\Users\navya\AppData\Local\Programs\Python\Python314\python.exe"

os.environ["PYSPARK_PYTHON"] = python_path
os.environ["PYSPARK_DRIVER_PYTHON"] = python_path

# ------------------------------------------------
# Dataset Path
# ------------------------------------------------

dataset_path = r"C:\Users\navya\OneDrive\Documents\Chronos\datasets\processed\ai4i_clean.csv"

graphs_folder = r"C:\Users\navya\OneDrive\Documents\Chronos\graphs"

os.makedirs(graphs_folder, exist_ok=True)

# ------------------------------------------------
# Create Spark Session
# ------------------------------------------------

print("\nCreating Spark Session...")

spark = (
    SparkSession.builder
    .appName("Chronos AI - Feature Relationship Analysis")
    .master("local[*]")
    .config("spark.driver.host", "127.0.0.1")
    .config("spark.driver.bindAddress", "127.0.0.1")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

print("Spark Session Created Successfully")

# ------------------------------------------------
# Load Dataset
# ------------------------------------------------

print("\nLoading Dataset...")

df = spark.read.csv(
    dataset_path,
    header=True,
    inferSchema=True
)

print("Dataset Loaded Successfully")

# ------------------------------------------------
# Select Numerical Features
# ------------------------------------------------

features = [
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]"
]

target = "Machine failure"

# ------------------------------------------------
# 1. Correlation with Machine Failure
# ------------------------------------------------

print("\n" + "=" * 60)
print("1. FEATURE CORRELATION WITH MACHINE FAILURE")
print("=" * 60)

correlations = []

for feature in features:
    value = df.stat.corr(feature, target)
    correlations.append((feature, value))

    print(
        f"{feature} -> Correlation: {value:.4f}"
    )

# ------------------------------------------------
# 2. Display Correlation Ranking
# ------------------------------------------------

print("\n" + "=" * 60)
print("2. CORRELATION RANKING")
print("=" * 60)

correlations_sorted = sorted(
    correlations,
    key=lambda x: abs(x[1]),
    reverse=True
)

for index, (feature, value) in enumerate(
    correlations_sorted,
    start=1
):
    print(
        f"{index}. {feature} -> {value:.4f}"
    )

# ------------------------------------------------
# 3. Create Correlation Chart
# ------------------------------------------------

print("\n" + "=" * 60)
print("3. GENERATING CORRELATION CHART")
print("=" * 60)

short_names = [
    "Air Temperature",
    "Process Temperature",
    "Rotational Speed",
    "Torque",
    "Tool Wear"
]

correlation_values = []

for feature in features:
    value = df.stat.corr(feature, target)
    correlation_values.append(value)

plt.figure(figsize=(9, 5))

plt.bar(
    short_names,
    correlation_values
)

plt.axhline(
    y=0,
    linewidth=0.8
)

plt.title(
    "Feature Correlation with Machine Failure"
)

plt.xlabel("Features")
plt.ylabel("Correlation Coefficient")

plt.xticks(rotation=15)

plt.tight_layout()

correlation_graph = os.path.join(
    graphs_folder,
    "feature_failure_correlation.png"
)

plt.savefig(
    correlation_graph,
    dpi=300
)

plt.show()
plt.close()

print(
    "\nCorrelation graph saved:"
)
print(correlation_graph)

# ------------------------------------------------
# 4. Strongest Relationship
# ------------------------------------------------

print("\n" + "=" * 60)
print("4. STRONGEST FEATURE RELATIONSHIP")
print("=" * 60)

strongest_feature, strongest_value = correlations_sorted[0]

print(
    "Strongest observed relationship:"
)

print(
    f"{strongest_feature} -> {strongest_value:.4f}"
)

# ------------------------------------------------
# 5. Feature-to-Feature Correlation
# ------------------------------------------------

print("\n" + "=" * 60)
print("5. FEATURE-TO-FEATURE RELATIONSHIPS")
print("=" * 60)

for i in range(len(features)):
    for j in range(i + 1, len(features)):

        feature_a = features[i]
        feature_b = features[j]

        value = df.stat.corr(
            feature_a,
            feature_b
        )

        print(
            f"{feature_a} <-> {feature_b} : {value:.4f}"
        )

# ------------------------------------------------
# 6. Final Findings
# ------------------------------------------------

print("\n" + "=" * 60)
print("6. KEY FINDINGS")
print("=" * 60)

print(
    "• Numerical features were analyzed against machine failure."
)

print(
    "• Correlation coefficients were calculated."
)

print(
    "• Features were ranked according to absolute correlation."
)

print(
    "• The strongest observed relationship was identified."
)

print(
    "• Feature-to-feature relationships were also analyzed."
)

print(
    "• Correlation results can support future feature selection."
)

# ------------------------------------------------
# Final Status
# ------------------------------------------------

print("\n" + "=" * 60)
print("FEATURE RELATIONSHIP ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 60)

spark.stop()

print("\nSpark Session Stopped Successfully")
print("DAY 42 COMPLETED SUCCESSFULLY")

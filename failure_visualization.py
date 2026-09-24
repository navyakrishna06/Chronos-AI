# ==========================================
# CHRONOS AI
# Day 41 - Failure Data Visualization
# ==========================================

import os
import matplotlib.pyplot as plt

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, sum

print("=" * 60)
print("          CHRONOS AI - DAY 41")
print("        FAILURE DATA VISUALIZATION")
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

# ------------------------------------------------
# Create Spark Session
# ------------------------------------------------

print("\nCreating Spark Session...")

spark = (
    SparkSession.builder
    .appName("Chronos AI - Failure Visualization")
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
# Create Graphs Folder
# ------------------------------------------------

graphs_folder = r"C:\Users\navya\OneDrive\Documents\Chronos\graphs"

os.makedirs(graphs_folder, exist_ok=True)

# ------------------------------------------------
# 1. Normal vs Failed Machines
# ------------------------------------------------

print("\n" + "=" * 60)
print("1. NORMAL VS FAILED MACHINES")
print("=" * 60)

normal_count = df.filter(col("Machine failure") == 0).count()
failure_count = df.filter(col("Machine failure") == 1).count()

print("Normal Machines :", normal_count)
print("Failed Machines :", failure_count)

plt.figure(figsize=(7, 5))

plt.bar(
    ["Normal", "Failed"],
    [normal_count, failure_count]
)

plt.title("Normal vs Failed Machines")
plt.xlabel("Machine Status")
plt.ylabel("Number of Machines")

plt.tight_layout()

plt.savefig(
    os.path.join(graphs_folder, "normal_vs_failed.png"),
    dpi=300
)

plt.show()
plt.close()

# ------------------------------------------------
# 2. Torque Comparison
# ------------------------------------------------

print("\n" + "=" * 60)
print("2. TORQUE COMPARISON")
print("=" * 60)

torque_data = df.groupBy("Machine failure").agg(
    avg("Torque [Nm]").alias("Average Torque")
).orderBy("Machine failure")

torque_rows = torque_data.collect()

normal_torque = torque_rows[0]["Average Torque"]
failure_torque = torque_rows[1]["Average Torque"]

print("Normal Average Torque :", round(normal_torque, 2))
print("Failed Average Torque :", round(failure_torque, 2))

plt.figure(figsize=(7, 5))

plt.bar(
    ["Normal", "Failed"],
    [normal_torque, failure_torque]
)

plt.title("Average Torque Comparison")
plt.xlabel("Machine Status")
plt.ylabel("Average Torque (Nm)")

plt.tight_layout()

plt.savefig(
    os.path.join(graphs_folder, "torque_comparison.png"),
    dpi=300
)

plt.show()
plt.close()

# ------------------------------------------------
# 3. Tool Wear Comparison
# ------------------------------------------------

print("\n" + "=" * 60)
print("3. TOOL WEAR COMPARISON")
print("=" * 60)

wear_data = df.groupBy("Machine failure").agg(
    avg("Tool wear [min]").alias("Average Tool Wear")
).orderBy("Machine failure")

wear_rows = wear_data.collect()

normal_wear = wear_rows[0]["Average Tool Wear"]
failure_wear = wear_rows[1]["Average Tool Wear"]

print("Normal Average Tool Wear :", round(normal_wear, 2))
print("Failed Average Tool Wear :", round(failure_wear, 2))

plt.figure(figsize=(7, 5))

plt.bar(
    ["Normal", "Failed"],
    [normal_wear, failure_wear]
)

plt.title("Average Tool Wear Comparison")
plt.xlabel("Machine Status")
plt.ylabel("Average Tool Wear (min)")

plt.tight_layout()

plt.savefig(
    os.path.join(graphs_folder, "tool_wear_comparison.png"),
    dpi=300
)

plt.show()
plt.close()

# ------------------------------------------------
# 4. Rotational Speed Comparison
# ------------------------------------------------

print("\n" + "=" * 60)
print("4. ROTATIONAL SPEED COMPARISON")
print("=" * 60)

speed_data = df.groupBy("Machine failure").agg(
    avg("Rotational speed [rpm]").alias("Average Speed")
).orderBy("Machine failure")

speed_rows = speed_data.collect()

normal_speed = speed_rows[0]["Average Speed"]
failure_speed = speed_rows[1]["Average Speed"]

print("Normal Average Speed :", round(normal_speed, 2))
print("Failed Average Speed :", round(failure_speed, 2))

plt.figure(figsize=(7, 5))

plt.bar(
    ["Normal", "Failed"],
    [normal_speed, failure_speed]
)

plt.title("Average Rotational Speed Comparison")
plt.xlabel("Machine Status")
plt.ylabel("Average Rotational Speed (rpm)")

plt.tight_layout()

plt.savefig(
    os.path.join(graphs_folder, "rotational_speed_comparison.png"),
    dpi=300
)

plt.show()
plt.close()

# ------------------------------------------------
# 5. Failure Reasons
# ------------------------------------------------

print("\n" + "=" * 60)
print("5. FAILURE REASON ANALYSIS")
print("=" * 60)

reason_data = df.select(
    sum("TWF").alias("TWF"),
    sum("HDF").alias("HDF"),
    sum("PWF").alias("PWF"),
    sum("OSF").alias("OSF"),
    sum("RNF").alias("RNF")
).collect()[0]

reasons = [
    "Tool Wear",
    "Heat Dissipation",
    "Power",
    "Overstrain",
    "Random"
]

reason_counts = [
    reason_data["TWF"],
    reason_data["HDF"],
    reason_data["PWF"],
    reason_data["OSF"],
    reason_data["RNF"]
]

print("Tool Wear Failure       :", reason_data["TWF"])
print("Heat Dissipation Failure:", reason_data["HDF"])
print("Power Failure           :", reason_data["PWF"])
print("Overstrain Failure      :", reason_data["OSF"])
print("Random Failure          :", reason_data["RNF"])

plt.figure(figsize=(8, 5))

plt.bar(
    reasons,
    reason_counts
)

plt.title("Failure Reasons Distribution")
plt.xlabel("Failure Type")
plt.ylabel("Number of Occurrences")

plt.xticks(rotation=15)

plt.tight_layout()

plt.savefig(
    os.path.join(graphs_folder, "failure_reasons.png"),
    dpi=300
)

plt.show()
plt.close()

# ------------------------------------------------
# 6. Machine Type Failure
# ------------------------------------------------

print("\n" + "=" * 60)
print("6. MACHINE TYPE FAILURE")
print("=" * 60)

type_data = (
    df.filter(col("Machine failure") == 1)
      .groupBy("Type")
      .count()
      .orderBy(col("count").desc())
)

type_rows = type_data.collect()

machine_types = [row["Type"] for row in type_rows]
type_counts = [row["count"] for row in type_rows]

for row in type_rows:
    print(
        "Type", row["Type"],
        "Failure Count:", row["count"]
    )

plt.figure(figsize=(7, 5))

plt.bar(
    machine_types,
    type_counts
)

plt.title("Machine Type Failure Distribution")
plt.xlabel("Machine Type")
plt.ylabel("Number of Failures")

plt.tight_layout()

plt.savefig(
    os.path.join(graphs_folder, "machine_type_failures.png"),
    dpi=300
)

plt.show()
plt.close()

# ------------------------------------------------
# Final Status
# ------------------------------------------------

print("\n" + "=" * 60)
print("ALL VISUALIZATIONS GENERATED SUCCESSFULLY")
print("=" * 60)

print("\nGraphs saved in:")
print(graphs_folder)

spark.stop()

print("\nSpark Session Stopped Successfully")
print("DAY 41 COMPLETED SUCCESSFULLY")

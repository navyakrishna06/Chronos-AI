# ==========================================
# CHRONOS AI
# Day 40 - Failure Pattern & Feature Analysis
# ==========================================

import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    avg,
    min,
    max,
    round
)

print("=" * 60)
print("          CHRONOS AI - DAY 40")
print("       FAILURE PATTERN ANALYSIS")
print("=" * 60)

# Python configuration
python_path = r"C:\Users\navya\AppData\Local\Programs\Python\Python314\python.exe"

os.environ["PYSPARK_PYTHON"] = python_path
os.environ["PYSPARK_DRIVER_PYTHON"] = python_path

# Dataset path
dataset_path = r"C:\Users\navya\OneDrive\Documents\Chronos\datasets\processed\ai4i_clean.csv"

# ------------------------------------------------
# 1. Create Spark Session
# ------------------------------------------------

print("\nCreating Spark Session...")

spark = (
    SparkSession.builder
    .appName("Chronos AI - Failure Pattern Analysis")
    .master("local[*]")
    .config("spark.driver.host", "127.0.0.1")
    .config("spark.driver.bindAddress", "127.0.0.1")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

print("Spark Session Created Successfully")

# ------------------------------------------------
# 2. Load Dataset
# ------------------------------------------------

print("\nLoading Dataset...")

df = spark.read.csv(
    dataset_path,
    header=True,
    inferSchema=True
)

print("Dataset Loaded Successfully")

# ------------------------------------------------
# 3. Separate Normal and Failed Machines
# ------------------------------------------------

print("\n" + "=" * 60)
print("1. NORMAL VS FAILED MACHINES")
print("=" * 60)

normal_df = df.filter(col("Machine failure") == 0)
failure_df = df.filter(col("Machine failure") == 1)

print("Normal Machines :", normal_df.count())
print("Failed Machines :", failure_df.count())

# ------------------------------------------------
# 4. Compare Average Parameters
# ------------------------------------------------

print("\n" + "=" * 60)
print("2. PARAMETER COMPARISON")
print("=" * 60)

comparison = df.groupBy("Machine failure").agg(
    round(avg("Air temperature [K]"), 2).alias("Avg Air Temperature"),
    round(avg("Process temperature [K]"), 2).alias("Avg Process Temperature"),
    round(avg("Rotational speed [rpm]"), 2).alias("Avg Rotational Speed"),
    round(avg("Torque [Nm]"), 2).alias("Avg Torque"),
    round(avg("Tool wear [min]"), 2).alias("Avg Tool Wear")
).orderBy("Machine failure")

print("\n0 = Normal | 1 = Failed\n")

comparison.show(truncate=False)

# ------------------------------------------------
# 5. Normal Machine Statistics
# ------------------------------------------------

print("\n" + "=" * 60)
print("3. NORMAL MACHINE STATISTICS")
print("=" * 60)

normal_stats = normal_df.select(
    round(avg("Air temperature [K]"), 2).alias("Average Air Temperature"),
    round(avg("Process temperature [K]"), 2).alias("Average Process Temperature"),
    round(avg("Rotational speed [rpm]"), 2).alias("Average Rotational Speed"),
    round(avg("Torque [Nm]"), 2).alias("Average Torque"),
    round(avg("Tool wear [min]"), 2).alias("Average Tool Wear")
)

normal_stats.show(truncate=False)

# ------------------------------------------------
# 6. Failed Machine Statistics
# ------------------------------------------------

print("\n" + "=" * 60)
print("4. FAILED MACHINE STATISTICS")
print("=" * 60)

failure_stats = failure_df.select(
    round(avg("Air temperature [K]"), 2).alias("Average Air Temperature"),
    round(avg("Process temperature [K]"), 2).alias("Average Process Temperature"),
    round(avg("Rotational speed [rpm]"), 2).alias("Average Rotational Speed"),
    round(avg("Torque [Nm]"), 2).alias("Average Torque"),
    round(avg("Tool wear [min]"), 2).alias("Average Tool Wear")
)

failure_stats.show(truncate=False)

# ------------------------------------------------
# 7. Minimum and Maximum Values
# ------------------------------------------------

print("\n" + "=" * 60)
print("5. DATA RANGE ANALYSIS")
print("=" * 60)

range_analysis = df.select(
    min("Air temperature [K]").alias("Min Air Temperature"),
    max("Air temperature [K]").alias("Max Air Temperature"),
    min("Process temperature [K]").alias("Min Process Temperature"),
    max("Process temperature [K]").alias("Max Process Temperature"),
    min("Rotational speed [rpm]").alias("Min Rotational Speed"),
    max("Rotational speed [rpm]").alias("Max Rotational Speed"),
    min("Torque [Nm]").alias("Min Torque"),
    max("Torque [Nm]").alias("Max Torque"),
    min("Tool wear [min]").alias("Min Tool Wear"),
    max("Tool wear [min]").alias("Max Tool Wear")
)

range_analysis.show(truncate=False)

# ------------------------------------------------
# 8. Failure Reason Distribution
# ------------------------------------------------

print("\n" + "=" * 60)
print("6. FAILURE INDICATOR ANALYSIS")
print("=" * 60)

failure_indicators = df.select(
    col("TWF").alias("Tool Wear Failure"),
    col("HDF").alias("Heat Dissipation Failure"),
    col("PWF").alias("Power Failure"),
    col("OSF").alias("Overstrain Failure"),
    col("RNF").alias("Random Failure")
)

indicator_totals = failure_indicators.agg(
    {"Tool Wear Failure": "sum",
     "Heat Dissipation Failure": "sum",
     "Power Failure": "sum",
     "Overstrain Failure": "sum",
     "Random Failure": "sum"}
)

indicator_totals.show(truncate=False)

# ------------------------------------------------
# 9. Machine Type Failure Analysis
# ------------------------------------------------

print("\n" + "=" * 60)
print("7. MACHINE TYPE FAILURE ANALYSIS")
print("=" * 60)

type_analysis = (
    failure_df
    .groupBy("Type")
    .count()
    .orderBy(col("count").desc())
)

type_analysis.show()

# ------------------------------------------------
# 10. High Tool Wear Analysis
# ------------------------------------------------

print("\n" + "=" * 60)
print("8. HIGH TOOL WEAR ANALYSIS")
print("=" * 60)

high_tool_wear = df.filter(col("Tool wear [min]") > 150)

print(
    "Machines with Tool Wear > 150 minutes:",
    high_tool_wear.count()
)

high_tool_wear.groupBy("Machine failure").count().show()

# ------------------------------------------------
# 11. High Torque Analysis
# ------------------------------------------------

print("\n" + "=" * 60)
print("9. HIGH TORQUE ANALYSIS")
print("=" * 60)

high_torque = df.filter(col("Torque [Nm]") > 50)

print(
    "Machines with Torque > 50 Nm:",
    high_torque.count()
)

high_torque.groupBy("Machine failure").count().show()

# ------------------------------------------------
# 12. Final Findings
# ------------------------------------------------

print("\n" + "=" * 60)
print("10. KEY FINDINGS")
print("=" * 60)

print("• Failed machines were identified successfully.")
print("• Normal and failed machine parameters were compared.")
print("• Temperature, speed, torque and tool wear were analyzed.")
print("• Failure indicators were analyzed.")
print("• Machine type failure distribution was analyzed.")
print("• High tool-wear and high-torque conditions were examined.")
print("• These patterns can support future predictive analysis.")

# ------------------------------------------------
# Final Status
# ------------------------------------------------

print("\n" + "=" * 60)
print("FAILURE PATTERN ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 60)

spark.stop()

print("\nSpark Session Stopped Successfully")
print("DAY 40 COMPLETED SUCCESSFULLY")
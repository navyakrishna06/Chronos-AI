# ==========================================
# CHRONOS AI
# Day 39 - PySpark Data Analysis
# ==========================================

import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, sum

print("=" * 60)
print("          CHRONOS AI - DAY 39")
print("          PYSPARK DATA ANALYSIS")
print("=" * 60)

# Python configuration
python_path = r"C:\Users\navya\AppData\Local\Programs\Python\Python314\python.exe"

os.environ["PYSPARK_PYTHON"] = python_path
os.environ["PYSPARK_DRIVER_PYTHON"] = python_path

# Dataset path
dataset_path = r"C:\Users\navya\OneDrive\Documents\Chronos\datasets\processed\ai4i_clean.csv"

print("\nCreating Spark Session...")

spark = (
    SparkSession.builder
    .appName("Chronos AI - PySpark Analysis")
    .master("local[*]")
    .config("spark.driver.host", "127.0.0.1")
    .config("spark.driver.bindAddress", "127.0.0.1")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

print("Spark Session Created Successfully")

# Load dataset
print("\nLoading Dataset...")

df = spark.read.csv(
    dataset_path,
    header=True,
    inferSchema=True
)

print("Dataset Loaded Successfully")

# ------------------------------------------------
# 1. Dataset Overview
# ------------------------------------------------

print("\n" + "=" * 60)
print("1. DATASET OVERVIEW")
print("=" * 60)

print("Total Records:", df.count())
print("Total Columns:", len(df.columns))

# ------------------------------------------------
# 2. Machine Failure Distribution
# ------------------------------------------------

print("\n" + "=" * 60)
print("2. MACHINE FAILURE DISTRIBUTION")
print("=" * 60)

failure_distribution = (
    df.groupBy("Machine failure")
      .count()
      .orderBy("Machine failure")
)

failure_distribution.show()

# ------------------------------------------------
# 3. Normal vs Failure Records
# ------------------------------------------------

print("\n" + "=" * 60)
print("3. NORMAL VS FAILURE")
print("=" * 60)

normal_count = df.filter(col("Machine failure") == 0).count()
failure_count = df.filter(col("Machine failure") == 1).count()

print("Normal Records :", normal_count)
print("Failure Records:", failure_count)

# ------------------------------------------------
# 4. Average Machine Parameters
# ------------------------------------------------

print("\n" + "=" * 60)
print("4. AVERAGE MACHINE PARAMETERS")
print("=" * 60)

df.select(
    avg("Air temperature [K]").alias("Average Air Temperature"),
    avg("Process temperature [K]").alias("Average Process Temperature"),
    avg("Rotational speed [rpm]").alias("Average Rotational Speed"),
    avg("Torque [Nm]").alias("Average Torque"),
    avg("Tool wear [min]").alias("Average Tool Wear")
).show(truncate=False)

# ------------------------------------------------
# 5. Failure Records
# ------------------------------------------------

print("\n" + "=" * 60)
print("5. FAILURE RECORDS")
print("=" * 60)

failure_records = df.filter(col("Machine failure") == 1)

print("Total Failure Records:", failure_records.count())

failure_records.select(
    "Type",
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]",
    "Machine failure"
).show(10, truncate=False)

# ------------------------------------------------
# 6. Failure Reason Analysis
# ------------------------------------------------

print("\n" + "=" * 60)
print("6. FAILURE REASON ANALYSIS")
print("=" * 60)

failure_reasons = df.select(
    sum("TWF").alias("Tool Wear Failures"),
    sum("HDF").alias("Heat Dissipation Failures"),
    sum("PWF").alias("Power Failures"),
    sum("OSF").alias("Overstrain Failures"),
    sum("RNF").alias("Random Failures")
)

failure_reasons.show(truncate=False)

# ------------------------------------------------
# 7. Failure by Machine Type
# ------------------------------------------------

print("\n" + "=" * 60)
print("7. FAILURE BY MACHINE TYPE")
print("=" * 60)

failure_by_type = (
    df.filter(col("Machine failure") == 1)
      .groupBy("Type")
      .count()
      .orderBy(col("count").desc())
)

failure_by_type.show()

# ------------------------------------------------
# 8. Parameter Analysis for Failed Machines
# ------------------------------------------------

print("\n" + "=" * 60)
print("8. FAILED MACHINE PARAMETER ANALYSIS")
print("=" * 60)

failure_records.select(
    avg("Air temperature [K]").alias("Avg Air Temperature"),
    avg("Process temperature [K]").alias("Avg Process Temperature"),
    avg("Rotational speed [rpm]").alias("Avg Rotational Speed"),
    avg("Torque [Nm]").alias("Avg Torque"),
    avg("Tool wear [min]").alias("Avg Tool Wear")
).show(truncate=False)

# ------------------------------------------------
# Final Status
# ------------------------------------------------

print("\n" + "=" * 60)
print("PYSPARK DATA ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 60)

spark.stop()

print("\nSpark Session Stopped Successfully")
print("DAY 39 COMPLETED SUCCESSFULLY")

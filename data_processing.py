# ==========================================
# CHRONOS AI
# Day 38 - Data Processing using PySpark
# ==========================================

import os
from pyspark.sql import SparkSession

print("=" * 50)
print("CHRONOS AI - DATA PROCESSING")
print("=" * 50)

# Python configuration for PySpark
python_path = r"C:\Users\navya\AppData\Local\Programs\Python\Python314\python.exe"

os.environ["PYSPARK_PYTHON"] = python_path
os.environ["PYSPARK_DRIVER_PYTHON"] = python_path

# Dataset path
dataset_path = r"C:\Users\navya\OneDrive\Documents\Chronos\datasets\processed\ai4i_clean.csv"

print("\nCreating Spark Session...")

spark = (
    SparkSession.builder
    .appName("Chronos AI - Data Processing")
    .master("local[*]")
    .config("spark.driver.host", "127.0.0.1")
    .config("spark.driver.bindAddress", "127.0.0.1")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

print("Spark Session Created Successfully")

# Check dataset
if not os.path.exists(dataset_path):
    print("\nERROR: Dataset not found!")
    print(dataset_path)
    spark.stop()
    exit()

# Load Dataset
print("\nLoading AI4I cleaned dataset...")

df = spark.read.csv(
    dataset_path,
    header=True,
    inferSchema=True
)

print("\nDataset Loaded Successfully")

# Dataset information
print("\n" + "=" * 50)
print("DATASET INFORMATION")
print("=" * 50)

print("\nTotal Rows:", df.count())
print("Total Columns:", len(df.columns))

print("\nColumn Names:")
for column in df.columns:
    print("-", column)

print("\nDataset Schema:")
df.printSchema()

print("\nFirst 5 Records:")
df.show(5, truncate=False)

# Basic data processing
print("\n" + "=" * 50)
print("BASIC DATA PROCESSING")
print("=" * 50)

print("\nNumber of Partitions:", df.rdd.getNumPartitions())

print("\nDataset Summary:")
df.describe().show()

print("\n" + "=" * 50)
print("PYSPARK DATA PROCESSING COMPLETED SUCCESSFULLY")
print("=" * 50)

spark.stop()

print("\nSpark Session Stopped Successfully")
print("DAY 38 COMPLETED SUCCESSFULLY")
# ==========================================
# CHRONOS AI
# Day 37 - Spark Setup
# ==========================================

from pyspark.sql import SparkSession
import pyspark

print("=" * 50)
print("      CHRONOS AI - SPARK SETUP")
print("=" * 50)

print("\nCreating Spark Session...")

spark = SparkSession.builder \
    .appName("Chronos AI") \
    .master("local[*]") \
    .getOrCreate()

print("\nSpark Session Created Successfully")

print("\nSpark Information")
print("-----------------------------")
print("Application Name :", spark.sparkContext.appName)
print("Spark Version    :", spark.version)
print("PySpark Version  :", pyspark.__version__)

print("\nSpark Environment Ready")

spark.stop()

print("\nSpark Session Closed Successfully")
print("\nDay 37 Completed Successfully")
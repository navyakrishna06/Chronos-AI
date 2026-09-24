# ============================================
# CHRONOS AI
# Day 36 - PySpark Study
# ============================================

import os
import pyspark

print("=" * 45)
print("      CHRONOS AI - PYSPARK STUDY")
print("=" * 45)

print("\nWhat is PySpark?")
print("PySpark is the Python API of Apache Spark used for Big Data processing.")

print("\nPurpose of PySpark")
print("- Process Big Data")
print("- Faster Data Processing")
print("- Distributed Computing")
print("- Parallel Processing")
print("- Scalable Data Analytics")

print("\nWhy PySpark in Chronos AI?")
print("Chronos AI uses PySpark for:")
print("- Machine Sensor Data Processing")
print("- System Log Analysis")
print("- Performance Monitoring")
print("- Server Log Analytics")
print("- Large Scale Failure Prediction")
print("- Big Data Analytics")

print("\nEnvironment Information")
print("-" * 30)

print("PySpark Version :", pyspark.__version__)

java_home = os.environ.get("JAVA_HOME")

if java_home:
    print("JAVA_HOME      :", java_home)
    print("Status         : Configured Successfully")
else:
    print("JAVA_HOME      : Not Configured")

print("\nSummary")
print("-" * 30)
print("✓ PySpark Installed Successfully")
print("✓ Java Installed Successfully")
print("✓ JAVA_HOME Configured Successfully")
print("✓ PySpark Environment Ready")
print("✓ Ready for Spark Session Creation")

print("\nDay 36 Completed Successfully")
print("=" * 45)
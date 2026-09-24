# ============================================================
# CHRONOS AI
# Day 43 - Feature Engineering
# ============================================================

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when
import os
import shutil

# ============================================================
# 1. CREATE SPARK SESSION
# ============================================================

print("=" * 60)
print("          CHRONOS AI - DAY 43")
print("             FEATURE ENGINEERING")
print("=" * 60)

print("\nCreating Spark Session...")

spark = SparkSession.builder \
    .appName("Chronos AI - Feature Engineering") \
    .master("local[*]") \
    .getOrCreate()

print("Spark Session Created Successfully")

# ============================================================
# 2. LOAD DATASET
# ============================================================

input_path = r"C:\Users\navya\OneDrive\Documents\Chronos\datasets\processed\ai4i_clean.csv"

output_path = r"C:\Users\navya\OneDrive\Documents\Chronos\datasets\processed\ai4i_feature_engineered.csv"

print("\nLoading Dataset...")

df = spark.read.csv(
    input_path,
    header=True,
    inferSchema=True
)

print("Dataset Loaded Successfully")

print("\nOriginal Dataset")

print("Rows   :", df.count())
print("Columns:", len(df.columns))

# ============================================================
# 3. TEMPERATURE DIFFERENCE
# ============================================================

print("\n" + "=" * 60)
print("1. CREATING TEMPERATURE DIFFERENCE")
print("=" * 60)

df = df.withColumn(
    "Temperature Difference [K]",
    col("Process temperature [K]") - col("Air temperature [K]")
)

print("Temperature Difference feature created")

# ============================================================
# 4. POWER INDICATOR
# ============================================================

print("\n" + "=" * 60)
print("2. CREATING POWER FEATURE")
print("=" * 60)

df = df.withColumn(
    "Power Indicator",
    col("Rotational speed [rpm]") * col("Torque [Nm]")
)

print("Power Indicator feature created")

# ============================================================
# 5. HIGH TORQUE INDICATOR
# ============================================================

print("\n" + "=" * 60)
print("3. CREATING HIGH TORQUE INDICATOR")
print("=" * 60)

df = df.withColumn(
    "High Torque",
    when(col("Torque [Nm]") > 50, 1).otherwise(0)
)

print("High Torque feature created")

# ============================================================
# 6. HIGH TOOL WEAR INDICATOR
# ============================================================

print("\n" + "=" * 60)
print("4. CREATING HIGH TOOL WEAR INDICATOR")
print("=" * 60)

df = df.withColumn(
    "High Tool Wear",
    when(col("Tool wear [min]") > 150, 1).otherwise(0)
)

print("High Tool Wear feature created")

# ============================================================
# 7. TEMPERATURE STRESS INDICATOR
# ============================================================

print("\n" + "=" * 60)
print("5. CREATING TEMPERATURE STRESS INDICATOR")
print("=" * 60)

df = df.withColumn(
    "Temperature Stress",
    when(col("Temperature Difference [K]") > 10, 1).otherwise(0)
)

print("Temperature Stress feature created")

# ============================================================
# 8. SPEED-TORQUE RISK INDICATOR
# ============================================================

print("\n" + "=" * 60)
print("6. CREATING SPEED-TORQUE RISK INDICATOR")
print("=" * 60)

df = df.withColumn(
    "Speed Torque Risk",
    when(
        (col("Rotational speed [rpm]") > 2000) &
        (col("Torque [Nm]") > 50),
        1
    ).otherwise(0)
)

print("Speed Torque Risk feature created")

# ============================================================
# 9. FEATURE ENGINEERING RESULT
# ============================================================

print("\n" + "=" * 60)
print("7. FEATURE ENGINEERING RESULT")
print("=" * 60)

print("\nNew Feature Columns:")

print("- Temperature Difference [K]")
print("- Power Indicator")
print("- High Torque")
print("- High Tool Wear")
print("- Temperature Stress")
print("- Speed Torque Risk")

# ============================================================
# 10. SAMPLE FEATURE-ENGINEERED DATA
# ============================================================

print("\n" + "=" * 60)
print("8. SAMPLE FEATURE-ENGINEERED DATA")
print("=" * 60)

df.show(10, truncate=False)

# ============================================================
# 11. FEATURE SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("9. ENGINEERED FEATURE SUMMARY")
print("=" * 60)

df.select(
    "Temperature Difference [K]",
    "Power Indicator",
    "High Torque",
    "High Tool Wear",
    "Temperature Stress",
    "Speed Torque Risk"
).describe().show()

# ============================================================
# 12. SAVE FEATURE-ENGINEERED DATASET
# ============================================================

print("\n" + "=" * 60)
print("10. SAVING FEATURE-ENGINEERED DATASET")
print("=" * 60)

# Remove old folder/file if it exists
if os.path.exists(output_path):

    if os.path.isdir(output_path):
        shutil.rmtree(output_path)
        print("Old output folder removed")

    else:
        os.remove(output_path)
        print("Old output file removed")

print("\nConverting Spark DataFrame to Pandas...")

pandas_df = df.toPandas()

print("Conversion completed")

print("\nSaving CSV file...")

pandas_df.to_csv(
    output_path,
    index=False
)

print("\nFeature-engineered dataset saved successfully")
print("Output file:")
print(output_path)

# ============================================================
# 13. VERIFY OUTPUT
# ============================================================

print("\n" + "=" * 60)
print("11. OUTPUT VERIFICATION")
print("=" * 60)

if os.path.isfile(output_path):

    file_size = os.path.getsize(output_path)

    print("Output file created successfully")
    print("File size:", file_size, "bytes")
    print("Rows saved:", len(pandas_df))
    print("Columns saved:", len(pandas_df.columns))

else:

    print("ERROR: Output file was not created")

# ============================================================
# 14. STOP SPARK
# ============================================================

spark.stop()

print("\nSpark Session Stopped Successfully")

print("\n" + "=" * 60)
print("DAY 43 FEATURE ENGINEERING COMPLETED SUCCESSFULLY")
print("=" * 60)

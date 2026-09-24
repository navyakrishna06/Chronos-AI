from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# ============================================================
#           CHRONOS AI - DAY 45
#        ML DATASET PREPARATION
# ============================================================

print("=" * 60)
print("          CHRONOS AI - DAY 45")
print("       ML DATASET PREPARATION")
print("=" * 60)

# ------------------------------------------------------------
# 1. CREATE SPARK SESSION
# ------------------------------------------------------------

print("\nCreating Spark Session...")

spark = (
    SparkSession.builder
    .appName("Chronos_AI_Day45_ML_Dataset_Preparation")
    .config("spark.sql.ansi.enabled", "false")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

print("Spark Session Created Successfully")

# ------------------------------------------------------------
# 2. FILE PATHS
# ------------------------------------------------------------

input_path = (
    r"C:\Users\navya\OneDrive\Documents\Chronos"
    r"\datasets\processed\ai4i_selected_features.csv"
)

train_output = (
    r"C:\Users\navya\OneDrive\Documents\Chronos"
    r"\datasets\processed\ml_train.csv"
)

test_output = (
    r"C:\Users\navya\OneDrive\Documents\Chronos"
    r"\datasets\processed\ml_test.csv"
)

# ------------------------------------------------------------
# 3. LOAD DATASET
# ------------------------------------------------------------

print("\nLoading Selected Feature Dataset...")

df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(input_path)
)

print("Dataset Loaded Successfully")

# ------------------------------------------------------------
# 4. DATASET INFORMATION
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("1. DATASET INFORMATION")
print("=" * 60)

print("Total Rows   :", df.count())
print("Total Columns:", len(df.columns))

print("\nAvailable Columns:")

for column in df.columns:
    print("-", column)

# ------------------------------------------------------------
# 5. IDENTIFY TARGET VARIABLE
# ------------------------------------------------------------

target = "Machine failure"

print("\n" + "=" * 60)
print("2. TARGET VARIABLE IDENTIFICATION")
print("=" * 60)

print("Target Variable:", target)

if target not in df.columns:
    print("\nERROR: Target variable not found!")
    spark.stop()
    raise SystemExit

# ------------------------------------------------------------
# 6. FEATURE IDENTIFICATION
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("3. FEATURE IDENTIFICATION")
print("=" * 60)

feature_columns = [
    column
    for column in df.columns
    if column != target
]

print("\nInput Features:")

for column in feature_columns:
    print("-", column)

print("\nTotal Input Features:", len(feature_columns))

# ------------------------------------------------------------
# 7. MISSING VALUE CHECK
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("4. MISSING VALUE CHECK")
print("=" * 60)

missing_found = False

for column in df.columns:

    missing_count = (
        df.filter(col(column).isNull()).count()
    )

    print(f"{column} -> Missing Values: {missing_count}")

    if missing_count > 0:
        missing_found = True

if not missing_found:
    print("\nNo missing values found.")

# ------------------------------------------------------------
# 8. DUPLICATE CHECK
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("5. DUPLICATE RECORD CHECK")
print("=" * 60)

total_rows = df.count()
distinct_rows = df.dropDuplicates().count()

duplicate_count = total_rows - distinct_rows

print("Total Records     :", total_rows)
print("Distinct Records  :", distinct_rows)
print("Duplicate Records :", duplicate_count)

# ------------------------------------------------------------
# 9. MACHINE FAILURE DISTRIBUTION
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("6. MACHINE FAILURE DISTRIBUTION")
print("=" * 60)

failure_distribution = (
    df.groupBy(target)
    .count()
    .orderBy(target)
)

failure_distribution.show()

# ------------------------------------------------------------
# 10. SEPARATE FEATURES AND TARGET
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("7. SEPARATING FEATURES AND TARGET")
print("=" * 60)

X = df.select(feature_columns)
y = df.select(target)

print("Feature Dataset Rows :", X.count())
print("Feature Dataset Columns :", len(X.columns))

print("Target Dataset Rows :", y.count())
print("Target Dataset Columns :", len(y.columns))

print("\nFeatures and target separated successfully.")

# ------------------------------------------------------------
# 11. PREPARE COMPLETE ML DATASET
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("8. PREPARING ML DATASET")
print("=" * 60)

ml_df = df.select(
    feature_columns + [target]
)

print("ML dataset prepared successfully.")

# ------------------------------------------------------------
# 12. TRAIN TEST SPLIT
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("9. TRAIN TEST SPLIT")
print("=" * 60)

train_df, test_df = ml_df.randomSplit(
    [0.8, 0.2],
    seed=42
)

train_count = train_df.count()
test_count = test_df.count()

print("Training Records :", train_count)
print("Testing Records  :", test_count)

print(
    "Training Percentage :",
    round((train_count / total_rows) * 100, 2),
    "%"
)

print(
    "Testing Percentage  :",
    round((test_count / total_rows) * 100, 2),
    "%"
)

# ------------------------------------------------------------
# 13. TRAINING DATA DISTRIBUTION
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("10. TRAINING DATA FAILURE DISTRIBUTION")
print("=" * 60)

train_df.groupBy(target).count().orderBy(target).show()

# ------------------------------------------------------------
# 14. TEST DATA DISTRIBUTION
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("11. TEST DATA FAILURE DISTRIBUTION")
print("=" * 60)

test_df.groupBy(target).count().orderBy(target).show()

# ------------------------------------------------------------
# 15. SAVE TRAINING DATA
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("12. SAVING TRAINING DATASET")
print("=" * 60)

train_pd = train_df.toPandas()

train_pd.to_csv(
    train_output,
    index=False
)

print("Training dataset saved successfully:")
print(train_output)

print("Training Rows   :", len(train_pd))
print("Training Columns:", len(train_pd.columns))

# ------------------------------------------------------------
# 16. SAVE TEST DATA
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("13. SAVING TEST DATASET")
print("=" * 60)

test_pd = test_df.toPandas()

test_pd.to_csv(
    test_output,
    index=False
)

print("Testing dataset saved successfully:")
print(test_output)

print("Testing Rows   :", len(test_pd))
print("Testing Columns:", len(test_pd.columns))

# ------------------------------------------------------------
# 17. FILE VERIFICATION
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("14. DATASET VERIFICATION")
print("=" * 60)

import os

if os.path.exists(train_output):
    print("ML Train CSV : CREATED SUCCESSFULLY")
    print(
        "Train File Size:",
        os.path.getsize(train_output),
        "bytes"
    )
else:
    print("ML Train CSV : NOT FOUND")

if os.path.exists(test_output):
    print("ML Test CSV  : CREATED SUCCESSFULLY")
    print(
        "Test File Size:",
        os.path.getsize(test_output),
        "bytes"
    )
else:
    print("ML Test CSV  : NOT FOUND")

# ------------------------------------------------------------
# 18. SAMPLE TRAINING DATA
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("15. SAMPLE TRAINING DATA")
print("=" * 60)

train_df.show(10, truncate=False)

# ------------------------------------------------------------
# 19. SAMPLE TEST DATA
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("16. SAMPLE TEST DATA")
print("=" * 60)

test_df.show(10, truncate=False)

# ------------------------------------------------------------
# 20. KEY FINDINGS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("17. KEY FINDINGS")
print("=" * 60)

print("• Selected feature dataset loaded successfully.")
print("• Machine failure identified as target variable.")
print("• Input features were separated from the target.")
print("• Missing values were checked successfully.")
print("• Duplicate records were checked successfully.")
print("• Machine failure distribution was analyzed.")
print("• Dataset was divided into training and testing data.")
print("• Training dataset contains approximately 80% of records.")
print("• Testing dataset contains approximately 20% of records.")
print("• ML training and testing datasets were saved.")
print("• Dataset is ready for model training.")

# ------------------------------------------------------------
# 21. COMPLETION
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("ML DATASET PREPARATION COMPLETED SUCCESSFULLY")
print("=" * 60)

spark.stop()

print("\nSpark Session Stopped Successfully")
print("DAY 45 COMPLETED SUCCESSFULLY")

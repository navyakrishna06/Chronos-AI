
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import os
import shutil
import glob

# ============================================================
# CHRONOS AI - DAY 44
# FEATURE SELECTION
# ============================================================

print("=" * 60)
print("          CHRONOS AI - DAY 44")
print("           FEATURE SELECTION")
print("=" * 60)

# ------------------------------------------------------------
# 1. CREATE SPARK SESSION
# ------------------------------------------------------------

print("\nCreating Spark Session...")

spark = (
    SparkSession.builder
    .appName("Chronos AI - Feature Selection")
    .config("spark.sql.ansi.enabled", "false")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

print("Spark Session Created Successfully")

# ------------------------------------------------------------
# 2. LOAD FEATURE-ENGINEERED DATASET
# ------------------------------------------------------------

input_path = (
    r"C:\Users\navya\OneDrive\Documents\Chronos"
    r"\datasets\processed\ai4i_feature_engineered.csv"
)

print("\nLoading Feature-Engineered Dataset...")

# ------------------------------------------------------------
# HANDLE SPARK OUTPUT DIRECTORY FROM DAY 43
# ------------------------------------------------------------

if os.path.isdir(input_path):
    print("Detected Spark output directory.")
    
    part_files = glob.glob(
        os.path.join(input_path, "part-*.csv")
    )

    if not part_files:
        print("ERROR: No CSV part file found inside feature-engineered dataset folder.")
        spark.stop()
        raise SystemExit

    input_file = part_files[0]

else:
    input_file = input_path

# ------------------------------------------------------------
# LOAD DATASET
# ------------------------------------------------------------

df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(input_file)
)

print("Dataset Loaded Successfully")

# ------------------------------------------------------------
# 3. DATASET INFORMATION
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("1. DATASET INFORMATION")
print("=" * 60)

total_rows = df.count()
total_columns = len(df.columns)

print(f"Total Rows   : {total_rows}")
print(f"Total Columns: {total_columns}")

print("\nAvailable Features:")

for feature in df.columns:
    print(f"- {feature}")

# ------------------------------------------------------------
# 4. IDENTIFY NUMERICAL FEATURES
# ------------------------------------------------------------

target = "Machine failure"

numerical_features = []

for field in df.schema.fields:

    if field.name != target:

        if field.dataType.simpleString() in [
            "int",
            "bigint",
            "double",
            "float",
            "long",
            "short"
        ]:
            numerical_features.append(field.name)

print("\n" + "=" * 60)
print("2. NUMERICAL FEATURE IDENTIFICATION")
print("=" * 60)

print(f"\nTarget Variable: {target}")

print("\nNumerical Features Selected:")

for feature in numerical_features:
    print(f"- {feature}")

# ------------------------------------------------------------
# 5. FEATURE CORRELATION
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("3. FEATURE CORRELATION WITH MACHINE FAILURE")
print("=" * 60)

correlation_results = []

for feature in numerical_features:

    try:

        # Check number of distinct values
        distinct_count = (
            df.select(feature)
            .where(col(feature).isNotNull())
            .distinct()
            .count()
        )

        # Constant features cannot have meaningful correlation
        if distinct_count <= 1:

            print(
                f"{feature} -> Skipped "
                f"(constant feature / zero variance)"
            )

            continue

        correlation_value = df.stat.corr(
            feature,
            target
        )

        if correlation_value is None:

            print(
                f"{feature} -> Skipped "
                f"(correlation unavailable)"
            )

            continue

        correlation_value = float(correlation_value)

        print(
            f"{feature} -> "
            f"Correlation: {correlation_value:.4f}"
        )

        correlation_results.append(
            (
                feature,
                correlation_value,
                abs(correlation_value)
            )
        )

    except Exception as e:

        print(
            f"{feature} -> Skipped "
            f"(unable to calculate correlation)"
        )

# ------------------------------------------------------------
# 6. CORRELATION RANKING
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("4. FEATURE CORRELATION RANKING")
print("=" * 60)

correlation_results.sort(
    key=lambda x: x[2],
    reverse=True
)

if len(correlation_results) > 0:

    for index, result in enumerate(
        correlation_results,
        start=1
    ):

        feature = result[0]
        correlation = result[1]

        print(
            f"{index}. {feature} "
            f"-> {correlation:.4f}"
        )

else:

    print("No valid correlations found.")

# ------------------------------------------------------------
# 7. SELECT IMPORTANT FEATURES
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("5. SELECTED FEATURES")
print("=" * 60)

# Correlation threshold
threshold = 0.05

selected_features = []

for feature, correlation, absolute_value in correlation_results:

    if absolute_value >= threshold:

        selected_features.append(feature)

if selected_features:

    for feature in selected_features:

        print(f"- {feature}")

else:

    print("No features crossed the correlation threshold.")

# ------------------------------------------------------------
# 8. FEATURE SELECTION SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("6. FEATURE SELECTION SUMMARY")
print("=" * 60)

print(
    f"Total Numerical Features : "
    f"{len(numerical_features)}"
)

print(
    f"Valid Correlation Features: "
    f"{len(correlation_results)}"
)

print(
    f"Selected Important Features: "
    f"{len(selected_features)}"
)

# ------------------------------------------------------------
# 9. SAVE SELECTED DATASET
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("7. SAVING SELECTED FEATURE DATASET")
print("=" * 60)

processed_folder = (
    r"C:\Users\navya\OneDrive\Documents\Chronos"
    r"\datasets\processed"
)

output_path = os.path.join(
    processed_folder,
    "ai4i_selected_features.csv"
)

# ------------------------------------------------------------
# KEEP SELECTED FEATURES + TARGET
# ------------------------------------------------------------

final_columns = selected_features + [target]

selected_df = df.select(*final_columns)

# ------------------------------------------------------------
# WINDOWS-SAFE CSV SAVE
# ------------------------------------------------------------
# IMPORTANT:
# Do NOT use Spark .write.csv() here.
# It requires Hadoop winutils.exe on Windows.
# Instead, convert to Pandas and save using Python.
# ------------------------------------------------------------

print("\nPreparing CSV file...")

try:

    pandas_df = selected_df.toPandas()

    # Remove old CSV file if present
    if os.path.isfile(output_path):
        os.remove(output_path)

    # Remove accidental directory with same name
    if os.path.isdir(output_path):
        shutil.rmtree(output_path)

    pandas_df.to_csv(
        output_path,
        index=False,
        encoding="utf-8"
    )

    print(
        "\nSelected feature dataset saved successfully:"
    )

    print(output_path)

    print(
        f"Saved Rows   : {len(pandas_df)}"
    )

    print(
        f"Saved Columns: {len(pandas_df.columns)}"
    )

except Exception as e:

    print("\nERROR while saving selected dataset:")
    print(str(e))

# ------------------------------------------------------------
# 10. VERIFY SAVED FILE
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("8. SAVED FILE VERIFICATION")
print("=" * 60)

if os.path.isfile(output_path):

    file_size = os.path.getsize(output_path)

    print("CSV File Status : CREATED SUCCESSFULLY")
    print(f"File Size       : {file_size:,} bytes")
    print(f"File Location   : {output_path}")

else:

    print("CSV File Status : NOT CREATED")

# ------------------------------------------------------------
# 11. SHOW SELECTED DATA
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("9. SELECTED FEATURE DATA")
print("=" * 60)

selected_df.show(
    10,
    truncate=False
)

# ------------------------------------------------------------
# 12. KEY FINDINGS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("10. KEY FINDINGS")
print("=" * 60)

print(
    "• Numerical features were identified successfully."
)

print(
    "• Feature correlation with machine failure was calculated."
)

print(
    "• Constant features were safely skipped."
)

print(
    "• Features were ranked using absolute correlation."
)

print(
    "• Important features were selected using correlation threshold."
)

print(
    "• Selected features were saved as a CSV file."
)

print(
    "• The selected dataset is ready for future ML modeling."
)

print(
    "• Feature selection prepares the dataset for model training."
)

# ------------------------------------------------------------
# 13. COMPLETION
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("FEATURE SELECTION COMPLETED SUCCESSFULLY")
print("=" * 60)

spark.stop()

print("\nSpark Session Stopped Successfully")
print("DAY 44 COMPLETED SUCCESSFULLY")


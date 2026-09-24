import pandas as pd
import re

input_file = "datasets/raw/HDFS.log"
output_file = "datasets/processed/hdfs_clean.csv"

data = []

print("Reading HDFS logs...")

with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()

        if not line:
            continue

        parts = line.split()

        # Extract basic fields
        date = parts[0]
        time = parts[1]
        log_id = parts[2]
        level = parts[3]

        message = " ".join(parts[4:])

        # Extract block id
        block_id = re.findall(r"blk_-?\d+", message)

        data.append([
            date,
            time,
            log_id,
            level,
            block_id[0] if block_id else "NA",
            message
        ])

df = pd.DataFrame(data, columns=[
    "Date",
    "Time",
    "Log_ID",
    "Level",
    "Block_ID",
    "Message"
])

df.to_csv(output_file, index=False)

print("HDFS cleaning completed!")
print("Shape:", df.shape)
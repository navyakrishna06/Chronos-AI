import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

df = pd.read_csv("datasets/processed/ai4i_clean.csv")

os.makedirs("graphs", exist_ok=True)

# 1
plt.figure(figsize=(5,4))
sns.countplot(x="Machine failure", data=df)
plt.title("Machine Failure Distribution")
plt.savefig("graphs/graph1_machine_failure.png")
plt.close()

# 2
plt.figure(figsize=(6,4))
sns.histplot(df["Air temperature [K]"], bins=20)
plt.title("Air Temperature Distribution")
plt.savefig("graphs/graph2_air_temperature.png")
plt.close()

# 3
plt.figure(figsize=(6,4))
sns.histplot(df["Torque [Nm]"], bins=20)
plt.title("Torque Distribution")
plt.savefig("graphs/graph3_torque.png")
plt.close()

# 4
plt.figure(figsize=(6,4))
sns.histplot(df["Rotational speed [rpm]"], bins=20)
plt.title("Rotational Speed Distribution")
plt.savefig("graphs/graph4_rpm.png")
plt.close()

# 5
plt.figure(figsize=(8,6))
sns.heatmap(df.select_dtypes(include=["number"]).corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.savefig("graphs/graph5_heatmap.png")
plt.close()

print("✅ All 5 graphs saved successfully in the 'graphs' folder.")
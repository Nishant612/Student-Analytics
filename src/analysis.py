import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# ==========================================
# 1. LOAD DATA
# ==========================================

df = pd.read_csv("data/engineering_student_journey.csv")

print("\n========== DATASET LOADED ==========")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")


# ==========================================
# 2. FIRST LOOK
# ==========================================

print("\n========== FIRST 5 ROWS ==========")
print(df.head())


# ==========================================
# 3. COLUMN NAMES
# ==========================================

print("\n========== COLUMNS ==========")

for i, column in enumerate(df.columns, start=1):
    print(f"{i}. {column}")


# ==========================================
# 4. DATA TYPES & NON-NULL VALUES
# ==========================================

print("\n========== DATA INFO ==========")
df.info()


# ==========================================
# 5. MISSING VALUES
# ==========================================

print("\n========== MISSING VALUES ==========")

missing = df.isnull().sum()

missing = missing[missing > 0].sort_values(
    ascending=False
)

if len(missing) == 0:
    print("No missing values found.")
else:
    print(missing)


# ==========================================
# 6. DUPLICATES
# ==========================================

print("\n========== DUPLICATES ==========")

duplicates = df.duplicated().sum()

print(f"Duplicate rows: {duplicates}")


# ==========================================
# 7. NUMERICAL STATISTICS
# ==========================================

print("\n========== NUMERICAL STATISTICS ==========")

print(df.describe())


# ==========================================
# 8. CATEGORICAL COLUMNS
# ==========================================

print("\n========== CATEGORICAL COLUMNS ==========")

categorical_cols = df.select_dtypes(
    include=["object"]
).columns

print(list(categorical_cols))

for column in categorical_cols:

    print(f"\n--- {column} ---")

    print(
        df[column]
        .value_counts()
        .head(10)
    )


# ==========================================
# 9. FIND PLACEMENT COLUMN
# ==========================================

print("\n========== PLACEMENT COLUMNS ==========")

placement_columns = [
    column
    for column in df.columns
    if "placement" in column.lower()
]

print(placement_columns)


# ==========================================
# 10. CORRELATION
# ==========================================

print("\n========== CORRELATION MATRIX ==========")

numeric_df = df.select_dtypes(
    include=np.number
)

print(
    numeric_df.corr().round(2)
)


# ==========================================
# 11. CORRELATION HEATMAP
# ==========================================

plt.figure(figsize=(10, 7))

sns.heatmap(
    numeric_df.corr(),
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Correlation Matrix")

plt.tight_layout()

plt.show()
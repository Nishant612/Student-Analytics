import pandas as pd
import numpy as np
import os

# ============================================================
# STUDENT SUCCESS ANALYTICS
# STEP 4: DATA CLEANING
# ============================================================

# ------------------------------------------------------------
# 1. FILE PATHS
# ------------------------------------------------------------

INPUT_FILE = "data/engineering_student_journey.csv"
OUTPUT_FILE = "data/cleaned_student_data.csv"


# ------------------------------------------------------------
# 2. LOAD DATA
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("LOADING DATASET")
print("=" * 60)

if not os.path.exists(INPUT_FILE):
    print(f"ERROR: File not found: {INPUT_FILE}")
    print("Make sure the CSV is inside the 'data' folder.")
    exit()

df = pd.read_csv(INPUT_FILE)

print(f"Original rows    : {df.shape[0]}")
print(f"Original columns : {df.shape[1]}")


# ------------------------------------------------------------
# 3. CREATE A COPY
# ------------------------------------------------------------

clean_df = df.copy()


# ------------------------------------------------------------
# 4. DISPLAY ORIGINAL COLUMNS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("ORIGINAL COLUMNS")
print("=" * 60)

for i, column in enumerate(clean_df.columns, 1):
    print(f"{i}. {column}")


# ------------------------------------------------------------
# 5. CLEAN COLUMN NAMES
# ------------------------------------------------------------

clean_df.columns = (
    clean_df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_", regex=False)
    .str.replace("-", "_", regex=False)
    .str.replace("/", "_", regex=False)
    .str.replace("(", "", regex=False)
    .str.replace(")", "", regex=False)
)

print("\n" + "=" * 60)
print("CLEANED COLUMN NAMES")
print("=" * 60)

print(clean_df.columns.tolist())


# ------------------------------------------------------------
# 6. CHECK DUPLICATES
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("DUPLICATE CHECK")
print("=" * 60)

duplicate_count = clean_df.duplicated().sum()

print(f"Duplicate rows found: {duplicate_count}")

if duplicate_count > 0:
    clean_df = clean_df.drop_duplicates()
    print("Duplicates removed.")
else:
    print("No duplicate rows found.")


# ------------------------------------------------------------
# 7. CHECK MISSING VALUES BEFORE CLEANING
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("MISSING VALUES BEFORE CLEANING")
print("=" * 60)

missing_before = clean_df.isnull().sum()

missing_before = missing_before[
    missing_before > 0
].sort_values(ascending=False)

if len(missing_before) == 0:
    print("No missing values found.")
else:
    print(missing_before)


# ------------------------------------------------------------
# 8. CLEAN TEXT / CATEGORICAL COLUMNS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("CLEANING CATEGORICAL COLUMNS")
print("=" * 60)

categorical_columns = clean_df.select_dtypes(
    include=["object"]
).columns

print("Categorical columns:")

for column in categorical_columns:
    print(f" - {column}")

    # Convert to string
    clean_df[column] = clean_df[column].astype("string")

    # Remove leading/trailing spaces
    clean_df[column] = clean_df[column].str.strip()

    # Convert multiple spaces into one
    clean_df[column] = (
        clean_df[column]
        .str.replace(r"\s+", " ", regex=True)
    )


# ------------------------------------------------------------
# 9. HANDLE MISSING NUMERICAL VALUES
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("HANDLING NUMERICAL MISSING VALUES")
print("=" * 60)

numeric_columns = clean_df.select_dtypes(
    include=np.number
).columns

for column in numeric_columns:

    missing_count = clean_df[column].isnull().sum()

    if missing_count > 0:

        median_value = clean_df[column].median()

        clean_df[column] = clean_df[column].fillna(
            median_value
        )

        print(
            f"{column}: "
            f"{missing_count} missing values "
            f"filled with median = {median_value}"
        )


# ------------------------------------------------------------
# 10. HANDLE MISSING CATEGORICAL VALUES
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("HANDLING CATEGORICAL MISSING VALUES")
print("=" * 60)

categorical_columns = clean_df.select_dtypes(
    include=["object", "string"]
).columns

for column in categorical_columns:

    missing_count = clean_df[column].isnull().sum()

    if missing_count > 0:

        mode_values = clean_df[column].mode()

        if len(mode_values) > 0:

            mode_value = mode_values.iloc[0]

            clean_df[column] = clean_df[column].fillna(
                mode_value
            )

            print(
                f"{column}: "
                f"{missing_count} missing values "
                f"filled with mode = {mode_value}"
            )


# ------------------------------------------------------------
# 11. REMOVE EMPTY STRING VALUES
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("CHECKING EMPTY STRINGS")
print("=" * 60)

for column in categorical_columns:

    empty_count = (
        clean_df[column]
        .astype("string")
        .str.strip()
        .eq("")
        .sum()
    )

    if empty_count > 0:

        mode_values = clean_df[column].mode()

        if len(mode_values) > 0:

            clean_df.loc[
                clean_df[column]
                .astype("string")
                .str.strip()
                .eq(""),
                column
            ] = mode_values.iloc[0]

            print(
                f"{column}: "
                f"{empty_count} empty values replaced."
            )


# ------------------------------------------------------------
# 12. TRY TO CONVERT NUMERIC-LIKE COLUMNS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("CHECKING NUMERIC-LIKE COLUMNS")
print("=" * 60)

for column in clean_df.select_dtypes(
    include=["object", "string"]
).columns:

    # Remove percentage signs for testing
    temp = (
        clean_df[column]
        .astype("string")
        .str.replace("%", "", regex=False)
        .str.strip()
    )

    converted = pd.to_numeric(
        temp,
        errors="coerce"
    )

    # If at least 90% of non-null values are numeric,
    # treat the column as numeric.
    original_non_null = temp.notna().sum()

    if original_non_null > 0:

        numeric_count = converted.notna().sum()

        numeric_ratio = (
            numeric_count /
            original_non_null
        )

        if numeric_ratio >= 0.90:

            clean_df[column] = converted

            print(
                f"{column} -> converted to numeric"
            )


# ------------------------------------------------------------
# 13. RE-CHECK DATA TYPES
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("FINAL DATA TYPES")
print("=" * 60)

print(clean_df.dtypes)


# ------------------------------------------------------------
# 14. CHECK FOR REMAINING MISSING VALUES
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("MISSING VALUES AFTER CLEANING")
print("=" * 60)

missing_after = clean_df.isnull().sum()

missing_after = missing_after[
    missing_after > 0
].sort_values(ascending=False)

if len(missing_after) == 0:
    print("No missing values remain.")
else:
    print(missing_after)


# ------------------------------------------------------------
# 15. NUMERICAL SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("NUMERICAL SUMMARY")
print("=" * 60)

print(clean_df.describe())


# ------------------------------------------------------------
# 16. SEARCH FOR PLACEMENT-RELATED COLUMNS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("PLACEMENT-RELATED COLUMNS")
print("=" * 60)

placement_columns = [
    column
    for column in clean_df.columns
    if (
        "placement" in column.lower()
        or "placed" in column.lower()
    )
]

if placement_columns:
    for column in placement_columns:
        print(f"\nColumn: {column}")
        print(clean_df[column].value_counts(dropna=False))
else:
    print("No placement-related column automatically detected.")


# ------------------------------------------------------------
# 17. SEARCH FOR GPA-RELATED COLUMNS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("GPA-RELATED COLUMNS")
print("=" * 60)

gpa_columns = [
    column
    for column in clean_df.columns
    if (
        "gpa" in column.lower()
        or "cgpa" in column.lower()
    )
]

if gpa_columns:

    for column in gpa_columns:
        print(f"\nColumn: {column}")
        print(clean_df[column].describe())

else:
    print("No GPA-related column automatically detected.")


# ------------------------------------------------------------
# 18. SEARCH FOR ATTENDANCE-RELATED COLUMNS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("ATTENDANCE-RELATED COLUMNS")
print("=" * 60)

attendance_columns = [
    column
    for column in clean_df.columns
    if "attendance" in column.lower()
]

if attendance_columns:

    for column in attendance_columns:
        print(f"\nColumn: {column}")
        print(clean_df[column].describe())

else:
    print("No attendance column automatically detected.")


# ------------------------------------------------------------
# 19. FINAL DUPLICATE CHECK
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("FINAL DUPLICATE CHECK")
print("=" * 60)

print(
    "Remaining duplicates:",
    clean_df.duplicated().sum()
)


# ------------------------------------------------------------
# 20. FINAL DATASET SIZE
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("FINAL DATASET")
print("=" * 60)

print(f"Rows    : {clean_df.shape[0]}")
print(f"Columns : {clean_df.shape[1]}")


# ------------------------------------------------------------
# 21. SAVE CLEANED DATASET
# ------------------------------------------------------------

clean_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n" + "=" * 60)
print("SUCCESS")
print("=" * 60)

print(
    f"Cleaned dataset saved to:\n{OUTPUT_FILE}"
)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ============================================================
# STUDENT SUCCESS ANALYTICS
# STEP 5: EXPLORATORY DATA ANALYSIS
# ============================================================

INPUT_FILE = "data/cleaned_student_data.csv"
OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ------------------------------------------------------------
# 1. LOAD DATA
# ------------------------------------------------------------

df = pd.read_csv(INPUT_FILE)

print("=" * 70)
print("STUDENT SUCCESS ANALYTICS - EDA")
print("=" * 70)

print(f"\nRows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")


# ------------------------------------------------------------
# 2. BASIC INFORMATION
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("DATASET INFORMATION")
print("=" * 70)

print(df.info())


# ============================================================
# ANALYSIS 1
# PLACEMENT DISTRIBUTION
# ============================================================

placement_columns = [
    col for col in df.columns
    if "placement" in col.lower()
    or "placed" in col.lower()
]

if placement_columns:

    placement_col = placement_columns[0]

    print("\n" + "=" * 70)
    print("PLACEMENT DISTRIBUTION")
    print("=" * 70)

    placement_counts = df[placement_col].value_counts()

    print(placement_counts)

    plt.figure(figsize=(8, 5))

    sns.countplot(
        data=df,
        x=placement_col
    )

    plt.title("Student Placement Distribution")
    plt.xlabel("Placement Status")
    plt.ylabel("Number of Students")

    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/01_placement_distribution.png",
        dpi=300
    )

    plt.show()


# ============================================================
# ANALYSIS 2
# NUMERICAL DISTRIBUTIONS
# ============================================================

numeric_columns = df.select_dtypes(
    include=np.number
).columns

print("\n" + "=" * 70)
print("NUMERICAL COLUMNS")
print("=" * 70)

print(list(numeric_columns))


# ============================================================
# ANALYSIS 3
# CORRELATION HEATMAP
# ============================================================

if len(numeric_columns) >= 2:

    correlation = df[numeric_columns].corr()

    print("\n" + "=" * 70)
    print("CORRELATION MATRIX")
    print("=" * 70)

    print(correlation.round(2))

    plt.figure(figsize=(12, 8))

    sns.heatmap(
        correlation,
        annot=True,
        cmap="coolwarm",
        fmt=".2f"
    )

    plt.title("Correlation Between Numerical Variables")

    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/02_correlation_heatmap.png",
        dpi=300
    )

    plt.show()


# ============================================================
# ANALYSIS 4
# HISTOGRAMS
# ============================================================

for column in numeric_columns:

    plt.figure(figsize=(8, 5))

    sns.histplot(
        data=df,
        x=column,
        kde=True
    )

    plt.title(
        f"Distribution of {column.replace('_', ' ').title()}"
    )

    plt.xlabel(
        column.replace("_", " ").title()
    )

    plt.ylabel("Number of Students")

    plt.tight_layout()

    safe_name = column.replace(" ", "_")

    plt.savefig(
        f"{OUTPUT_DIR}/distribution_{safe_name}.png",
        dpi=300
    )

    plt.show()


# ============================================================
# ANALYSIS 5
# CATEGORICAL VARIABLES
# ============================================================

categorical_columns = df.select_dtypes(
    include=["object"]
).columns

print("\n" + "=" * 70)
print("CATEGORICAL VARIABLES")
print("=" * 70)

for column in categorical_columns:

    print(f"\n{column}")

    print(
        df[column]
        .value_counts()
        .head(15)
    )


# ============================================================
# ANALYSIS 6
# GPA / CGPA ANALYSIS
# ============================================================

gpa_columns = [
    col for col in df.columns
    if "gpa" in col.lower()
    or "cgpa" in col.lower()
]

if gpa_columns:

    gpa_col = gpa_columns[0]

    print("\n" + "=" * 70)
    print("GPA ANALYSIS")
    print("=" * 70)

    print(df[gpa_col].describe())

    plt.figure(figsize=(8, 5))

    sns.histplot(
        data=df,
        x=gpa_col,
        kde=True
    )

    plt.title("Distribution of Student GPA")

    plt.xlabel(
        gpa_col.replace("_", " ").title()
    )

    plt.ylabel("Number of Students")

    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/03_gpa_distribution.png",
        dpi=300
    )

    plt.show()


# ============================================================
# ANALYSIS 7
# ATTENDANCE VS GPA
# ============================================================

attendance_columns = [
    col for col in df.columns
    if "attendance" in col.lower()
]

if attendance_columns and gpa_columns:

    attendance_col = attendance_columns[0]
    gpa_col = gpa_columns[0]

    print("\n" + "=" * 70)
    print("ATTENDANCE VS GPA")
    print("=" * 70)

    correlation = df[
        [attendance_col, gpa_col]
    ].corr().iloc[0, 1]

    print(
        f"Correlation between "
        f"{attendance_col} and {gpa_col}: "
        f"{correlation:.3f}"
    )

    plt.figure(figsize=(8, 5))

    sns.scatterplot(
        data=df,
        x=attendance_col,
        y=gpa_col
    )

    sns.regplot(
        data=df,
        x=attendance_col,
        y=gpa_col,
        scatter=False
    )

    plt.title("Attendance vs GPA")

    plt.xlabel(
        attendance_col.replace("_", " ").title()
    )

    plt.ylabel(
        gpa_col.replace("_", " ").title()
    )

    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/04_attendance_vs_gpa.png",
        dpi=300
    )

    plt.show()


# ============================================================
# ANALYSIS 8
# GPA VS PLACEMENT
# ============================================================

if placement_columns and gpa_columns:

    placement_col = placement_columns[0]
    gpa_col = gpa_columns[0]

    print("\n" + "=" * 70)
    print("GPA VS PLACEMENT")
    print("=" * 70)

    print(
        df.groupby(placement_col)[gpa_col]
        .agg(["mean", "median", "min", "max"])
        .round(2)
    )

    plt.figure(figsize=(8, 5))

    sns.boxplot(
        data=df,
        x=placement_col,
        y=gpa_col
    )

    plt.title("GPA Distribution by Placement Status")

    plt.xlabel("Placement Status")

    plt.ylabel(
        gpa_col.replace("_", " ").title()
    )

    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/05_gpa_vs_placement.png",
        dpi=300
    )

    plt.show()


# ============================================================
# ANALYSIS 9
# ATTENDANCE VS PLACEMENT
# ============================================================

if placement_columns and attendance_columns:

    placement_col = placement_columns[0]
    attendance_col = attendance_columns[0]

    print("\n" + "=" * 70)
    print("ATTENDANCE VS PLACEMENT")
    print("=" * 70)

    print(
        df.groupby(placement_col)[attendance_col]
        .agg(["mean", "median", "min", "max"])
        .round(2)
    )

    plt.figure(figsize=(8, 5))

    sns.boxplot(
        data=df,
        x=placement_col,
        y=attendance_col
    )

    plt.title(
        "Attendance Distribution by Placement Status"
    )

    plt.xlabel("Placement Status")

    plt.ylabel(
        attendance_col.replace("_", " ").title()
    )

    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/06_attendance_vs_placement.png",
        dpi=300
    )

    plt.show()


# ============================================================
# ANALYSIS 10
# CATEGORICAL VARIABLES VS PLACEMENT
# ============================================================

if placement_columns:

    placement_col = placement_columns[0]

    for column in categorical_columns:

        if column == placement_col:
            continue

        # Avoid extremely high-cardinality columns
        unique_count = df[column].nunique()

        if unique_count <= 15:

            cross_tab = pd.crosstab(
                df[column],
                df[placement_col],
                normalize="index"
            ) * 100

            print("\n" + "=" * 70)
            print(f"{column.upper()} VS PLACEMENT")
            print("=" * 70)

            print(cross_tab.round(2))

            cross_tab.plot(
                kind="bar",
                figsize=(10, 6)
            )

            plt.title(
                f"{column.replace('_', ' ').title()} "
                f"vs Placement"
            )

            plt.xlabel(
                column.replace("_", " ").title()
            )

            plt.ylabel("Percentage")

            plt.xticks(rotation=45)

            plt.legend(
                title="Placement Status"
            )

            plt.tight_layout()

            safe_name = column.replace(" ", "_")

            plt.savefig(
                f"{OUTPUT_DIR}/placement_{safe_name}.png",
                dpi=300
            )

            plt.show()


# ============================================================
# ANALYSIS 11
# OUTLIER DETECTION
# ============================================================

print("\n" + "=" * 70)
print("OUTLIER ANALYSIS")
print("=" * 70)

for column in numeric_columns:

    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)

    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = df[
        (df[column] < lower_bound) |
        (df[column] > upper_bound)
    ]

    print(
        f"{column}: "
        f"{len(outliers)} potential outliers"
    )


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("EDA COMPLETE")
print("=" * 70)

print(
    f"\nGenerated visualizations are saved in: "
    f"{OUTPUT_DIR}/"
)

print("\nFiles generated:")

for file in sorted(os.listdir(OUTPUT_DIR)):
    print(f" - {file}")
import pandas as pd
import numpy as np
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

# --------------------------------------------------
# 1. Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "cleaned_student_data.csv"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

# --------------------------------------------------
# 2. Load data
# --------------------------------------------------

df = pd.read_csv(DATA_PATH)

print("Dataset loaded.")
print("Rows:", len(df))
print("Columns:", len(df.columns))

# --------------------------------------------------
# 3. Select features
# --------------------------------------------------

features = [
    "age",
    "gender",
    "branch",
    "average_gpa",
    "backlogs",
    "attendance_%",
    "clubs",
    "skills",
    "internship_done",
    "internship_domain"
]

target = "placement_status"

X = df[features].copy()
y = df[target].copy()

# --------------------------------------------------
# 4. Separate numerical and categorical features
# --------------------------------------------------

numerical_features = [
    "age",
    "average_gpa",
    "backlogs",
    "attendance_%"
]

categorical_features = [
    "gender",
    "branch",
    "clubs",
    "skills",
    "internship_done",
    "internship_domain"
]

# --------------------------------------------------
# 5. Preprocessing
# --------------------------------------------------

preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            "passthrough",
            numerical_features
        ),
        (
            "cat",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            ),
            categorical_features
        )
    ]
)

# --------------------------------------------------
# 6. Machine Learning model
# --------------------------------------------------

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)

# --------------------------------------------------
# 7. Train-test split
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))

# --------------------------------------------------
# 8. Train
# --------------------------------------------------

pipeline.fit(X_train, y_train)

# --------------------------------------------------
# 9. Predictions
# --------------------------------------------------

y_pred = pipeline.predict(X_test)

# --------------------------------------------------
# 10. Evaluation
# --------------------------------------------------

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(
    y_test,
    y_pred,
    pos_label="Placed"
)
recall = recall_score(
    y_test,
    y_pred,
    pos_label="Placed"
)
f1 = f1_score(
    y_test,
    y_pred,
    pos_label="Placed"
)

print("\n==============================")
print("MODEL PERFORMANCE")
print("==============================")

print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
cm = confusion_matrix(
    y_test,
    y_pred,
    labels=["Not Placed", "Placed"]
)

print(cm)

# --------------------------------------------------
# 11. Save metrics
# --------------------------------------------------

metrics = pd.DataFrame({
    "Metric": [
        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score"
    ],
    "Score": [
        accuracy,
        precision,
        recall,
        f1
    ]
})

metrics.to_csv(
    OUTPUT_DIR / "ml_metrics.csv",
    index=False
)

# --------------------------------------------------
# 12. Save confusion matrix
# --------------------------------------------------

cm_df = pd.DataFrame(
    cm,
    index=["Actual Not Placed", "Actual Placed"],
    columns=["Predicted Not Placed", "Predicted Placed"]
)

cm_df.to_csv(
    OUTPUT_DIR / "confusion_matrix.csv"
)

print("\nResults saved to outputs/")
print("- ml_metrics.csv")
print("- confusion_matrix.csv")
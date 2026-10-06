import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import os

# ============================================================
# LOAD CLEANED CSV
# ============================================================

df = pd.read_csv("data/cleaned_student_data.csv")

print("Dataset loaded.")
print("Rows:", len(df))
print("Columns:", len(df.columns))

# ============================================================
# MYSQL CONNECTION
# ============================================================
load_dotenv()

connection = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    port=int(os.getenv("MYSQL_PORT")),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE")
)

cursor = connection.cursor()

# ============================================================
# CREATE TABLE DYNAMICALLY
# ============================================================

columns = []

for column in df.columns:

    dtype = df[column].dtype

    if pd.api.types.is_integer_dtype(dtype):

        sql_type = "INT"

    elif pd.api.types.is_float_dtype(dtype):

        sql_type = "DOUBLE"

    else:

        sql_type = "VARCHAR(255)"

    columns.append(
        f"`{column}` {sql_type}"
    )


create_table_query = f"""
CREATE TABLE IF NOT EXISTS students (
    {", ".join(columns)}
);
"""

cursor.execute(create_table_query)

print("Table created successfully.")

# ============================================================
# INSERT DATA
# ============================================================

column_names = ", ".join(
    f"`{column}`"
    for column in df.columns
)

placeholders = ", ".join(
    ["%s"] * len(df.columns)
)

insert_query = f"""
INSERT INTO students ({column_names})
VALUES ({placeholders})
"""

data = []

for row in df.itertuples(
    index=False,
    name=None
):

    cleaned_row = []

    for value in row:

        if pd.isna(value):
            cleaned_row.append(None)
        else:
            cleaned_row.append(value)

    data.append(
        tuple(cleaned_row)
    )

cursor.executemany(
    insert_query,
    data
)

connection.commit()

print(
    f"{cursor.rowcount} rows inserted."
)

# ============================================================
# CLOSE CONNECTION
# ============================================================

cursor.close()
connection.close()

print("MySQL connection closed.")
print("Data successfully loaded into MySQL.")
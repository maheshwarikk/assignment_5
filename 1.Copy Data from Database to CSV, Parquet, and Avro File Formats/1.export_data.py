import pandas as pd
from sqlalchemy import create_engine
import pyarrow as pa
import pyarrow.parquet as pq
import fastavro

# CONFIGURATION 
MYSQL_USER = "root"
MYSQL_PASSWORD = "kallu"
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"
MYSQL_DB = "celebal_db"
QUERY = "SELECT * FROM employees;"


# Create SQLAlchemy engine
engine = create_engine(
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
)

# Read data from MySQL
df = pd.read_sql(QUERY, engine)

#  Export to CSV
df.to_csv("output.csv", index=False)
print(" Data exported to output.csv")

#  Export to Parquet
table = pa.Table.from_pandas(df)
pq.write_table(table, "output.parquet")
print(" Data exported to output.parquet")

#  Export to Avro
schema = {
    "doc": "Employee record",
    "name": "Employee",
    "namespace": "example.avro",
    "type": "record",
    "fields": [
        {"name": "id", "type": ["null", "int"]},
        {"name": "name", "type": ["null", "string"]},
        {"name": "department", "type": ["null", "string"]},
        {"name": "salary", "type": ["null", "float"]}  # salary is decimal, use float
    ]
}

# Replace NaNs with None for Avro compatibility
df = df.where(pd.notnull(df), None)

# Convert records with correct types
records = []
for _, row in df.iterrows():
    record = {
        "id": int(row["id"]) if row["id"] is not None else None,
        "name": row["name"],
        "department": row["department"],
        "salary": float(row["salary"]) if row["salary"] is not None else None,
    }
    records.append(record)

# Write to Avro
with open("output.avro", "wb") as out_file:
    fastavro.writer(out_file, schema, records)

print("Data exported to output.avro")

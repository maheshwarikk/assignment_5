from sqlalchemy import create_engine, text
import pandas as pd

#  DB Configs
SOURCE_DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "kallu",
    "database": "sakila"
}

DEST_DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "kallu",
    "database": "world"
}

#Tables and Columns
TABLES_TO_COPY = {
    "actor": ["actor_id", "first_name", "last_name"],
    "film": ["film_id", "title", "release_year", "language_id"],
    "language": ["language_id", "name"]
}

def get_engine(config):
    return create_engine(f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}/{config['database']}")

def copy_selected_columns():
    source_engine = get_engine(SOURCE_DB_CONFIG)
    dest_engine = get_engine(DEST_DB_CONFIG)

    for table, columns in TABLES_TO_COPY.items():
        print(f"\nCopying {table} with columns {columns}...")
        try:
            df = pd.read_sql(f"SELECT {', '.join(columns)} FROM {table}", source_engine)

            # Try inserting row-by-row with INSERT IGNORE or ON DUPLICATE KEY UPDATE
            with dest_engine.connect() as conn:
                for _, row in df.iterrows():
                    placeholders = ", ".join([f":{col}" for col in columns])
                    col_names = ", ".join(columns)
                    sql = f"INSERT IGNORE INTO {table} ({col_names}) VALUES ({placeholders})"
                    conn.execute(text(sql), row.to_dict())

            print(f"Copied rows to {table} (ignoring duplicates)")

        except Exception as e:
            print(f"Error copying {table}: {e}")

    print("\nSelective table/column migration complete.")

if __name__ == "__main__":
    copy_selected_columns()

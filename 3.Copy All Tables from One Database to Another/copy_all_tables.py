from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.exc import SQLAlchemyError

SOURCE_DB_URL = 'mysql+pymysql://root:kallu@localhost/sakila'
DEST_DB_URL   = 'mysql+pymysql://root:kallu@localhost/world'

source_engine = create_engine(SOURCE_DB_URL)
dest_engine = create_engine(DEST_DB_URL)

metadata = MetaData()
metadata.reflect(bind=source_engine)

SKIPPED_TABLES = set()

print("Starting to copy tables from sakila to world...\n")

for table_name, table in metadata.tables.items():
    print(f"Processing table: {table_name}")

    if table_name == "address":
        print(f" Skipping table '{table_name}' due to unsupported column types.")
        SKIPPED_TABLES.add(table_name)
        continue

    foreign_keys = [fk.column.table.name for fk in table.foreign_keys]
    if any(dep in SKIPPED_TABLES for dep in foreign_keys):
        print(f"Skipping '{table_name}' — depends on skipped table(s): {foreign_keys}")
        SKIPPED_TABLES.add(table_name)
        continue

    try:
        with dest_engine.connect() as conn:
            conn.execute(text(f"DROP TABLE IF EXISTS `{table_name}`"))
            conn.execute(text("SET foreign_key_checks = 0"))
            table.metadata.create_all(dest_engine, tables=[table])
            conn.execute(text("SET foreign_key_checks = 1"))

        with source_engine.connect() as source_conn:
            rows = source_conn.execute(table.select()).fetchall()
            data = [dict(row._mapping) for row in rows]

        if data:
            with dest_engine.connect() as dest_conn:
                dest_conn.execute(table.insert(), data)

        print(f"Copied table: {table_name} ({len(data)} rows)")

    except SQLAlchemyError as e:
        print(f"Error copying table '{table_name}': {e}")
        SKIPPED_TABLES.add(table_name)

print("\nAll table copy operations complete.")

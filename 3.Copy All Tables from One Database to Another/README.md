# Copy All Tables from One Database to Another (MySQL)

## Objective
To perform full database replication by dynamically identifying and copying all tables and their data from the source database (`sakila`) to the destination database (`world`). This process ensures complete schema and data consistency for backup, migration, or environment synchronization.

## Technologies Used
- Python 3.12
- SQLAlchemy
- PyMySQL
- MySQL Workbench and MySQL Server
- Visual Studio Code

## Features Implemented

| Feature               | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| Dynamic Table Discovery | Automatically detects all tables from the source database                 |
| Schema Replication    | Reconstructs each table’s structure in the destination database             |
| Data Copy             | Copies all rows from each table into the corresponding destination table    |
| Foreign Key Handling  | Skips tables that cannot be dropped or created due to foreign key issues    |
| Unsupported Types     | Skips tables with unsupported column types such as geometry                 |
| Error Logging         | Logs why a table was skipped or failed to copy                              |

## Source and Destination
- Source Database: sakila
- Destination Database: world

## Result Summary

| Table Name     | Status                                                       |
|----------------|--------------------------------------------------------------|
| actor          | Failed: Referenced by foreign key in film_actor              |
| address        | Skipped: Contains unsupported column type (geometry)         |
| city           | Failed: Missing referenced column in foreign key constraint  |
| country        | Failed: Referenced by foreign key in countrylanguage         |
| category       | Success (16 rows copied)                                     |
| customer       | Skipped: Depends on skipped tables (store, address)          |
| film_text      | Success (1000 rows copied)                                   |
| Others         | Skipped: Due to dependencies or foreign key constraints      |

## Notes
- The script is reusable with any MySQL databases by updating connection strings.
- Further improvements can include:
  - Foreign key constraint management
  - Retry mechanisms for dependent tables
  - Detailed logging to external files

## How to Run

Run the script using the command:


# Copy Selective Tables with Selective Columns from One Database to Another

## Objective
This script enables **selective data migration** by allowing users to specify:
- Which **tables** to copy from the source MySQL database
- Which **columns** to include from each selected table

This approach is useful for:
- Compliance (e.g., GDPR-safe migrations)
- Targeted analytics
- Lightweight backups or sampling
- Reduced data volume transfers

---

##  Features
-  Copy only **specified tables**
-  Copy only **selected columns**
-  Ignores existing duplicate entries (`INSERT IGNORE`)
-  Handles SQL errors gracefully
-  Easy to configure and reuse

---

##  Requirements

Install dependencies using:

```bash
pip install sqlalchemy pymysql

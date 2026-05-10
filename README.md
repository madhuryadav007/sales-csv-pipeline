# Sales CSV Pipeline

A beginner data engineering project that builds an end-to-end ETL pipeline in Python.

## What it does

- **Extracts** raw sales data from a CSV file (2823 rows, 25 columns)
- **Transforms** it by cleaning nulls, fixing data types, removing useless columns, and adding derived metrics
- **Loads** the clean data into both a CSV file and a SQLite database
- Logs every step with timestamps to both terminal and a log file

## Tech stack

- Python 3.11
- Pandas — data cleaning and transformation
- SQLite3 — local database storage
- Logging — pipeline observability

## Project structure
sales-csv-pipeline/
├── data/
│   └── sales_data_sample.csv    ← raw input
├── output/
│   ├── sales_clean.csv          ← cleaned CSV
│   └── sales.db                 ← SQLite database
├── src/
│   └── pipeline.py              ← main ETL script
├── pipeline.log                 ← auto-generated run logs
└── requirements.txt

## How to run

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/sales-csv-pipeline.git
cd sales-csv-pipeline

# 2. Create and activate virtual environment
python -m venv venv
source venv/Scripts/activate     # Windows Git Bash
source venv/bin/activate         # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add the dataset
# Download sales_data_sample.csv from Kaggle:
# https://www.kaggle.com/datasets/kyanyoga/sample-sales-data
# Place it in the data/ folder

# 5. Run the pipeline
python src/pipeline.py
```

## Sample output
2026-05-10 16:57:53 | INFO | === Pipeline started ===
2026-05-10 16:57:53 | INFO | Extracting: data/sales_data_sample.csv
2026-05-10 16:57:53 | INFO | Loaded 2823 rows, 25 columns
2026-05-10 16:57:53 | INFO | Starting transformations...
2026-05-10 16:57:53 | INFO | Kept 13 columns
2026-05-10 16:57:53 | INFO | Converted ORDERDATE to datetime
2026-05-10 16:57:53 | INFO | Filled nulls in STATE and TERRITORY
2026-05-10 16:57:53 | INFO | Removed 0 rows with zero/null SALES
2026-05-10 16:57:53 | INFO | Added YEAR, MONTH, REVENUE columns
2026-05-10 16:57:53 | INFO | Transform done. Final shape: (2823, 16)
2026-05-10 16:57:53 | INFO | === Pipeline completed in 0.09s ===
--- TOP 5 COUNTRIES BY SALES ---
USA             $ 3,627,982.83
SPAIN           $ 1,215,686.92
FRANCE          $ 1,110,916.52
AUSTRALIA       $   630,623.10
UK              $   478,880.46

## Transformations applied

1. Selected 13 relevant columns out of 25
2. Converted ORDERDATE from string to datetime
3. Filled missing STATE and TERRITORY values with 'Unknown'
4. Filtered out rows where SALES is zero
5. Added derived columns: YEAR, MONTH, REVENUE
6. Standardised COUNTRY and DEALSIZE to consistent casing

## Key learnings

- ETL pipeline design (Extract → Transform → Load)
- Pandas data cleaning — nulls, type conversion, derived columns
- SQLite database loading with Python
- Professional logging with timestamps
- Virtual environments and requirements.txt
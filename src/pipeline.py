import pandas as pd
import sqlite3
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("pipeline.log")
    ]
)

def extract(filepath):
    logging.info(f"Extracting: {filepath}")
    df = pd.read_csv(filepath, encoding='latin-1')
    logging.info(f"Loaded {len(df)} rows, {len(df.columns)} columns")
    return df

def transform(df):
    logging.info("Starting transformations...")

    cols = ['ORDERNUMBER', 'ORDERDATE', 'STATUS', 'PRODUCTLINE',
            'QUANTITYORDERED', 'PRICEEACH', 'SALES',
            'CUSTOMERNAME', 'CITY', 'COUNTRY', 'DEALSIZE',
            'STATE', 'TERRITORY']
    df = df[cols].copy()
    logging.info(f"Kept {len(cols)} columns")

    df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'])
    logging.info("Converted ORDERDATE to datetime")

    df['STATE']     = df['STATE'].fillna('Unknown')
    df['TERRITORY'] = df['TERRITORY'].fillna('Unknown')
    logging.info("Filled nulls in STATE and TERRITORY")

    before = len(df)
    df = df[df['SALES'] > 0]
    logging.info(f"Removed {before - len(df)} rows with zero/null SALES")

    df['YEAR']     = df['ORDERDATE'].dt.year
    df['MONTH']    = df['ORDERDATE'].dt.month
    df['REVENUE']  = df['QUANTITYORDERED'] * df['PRICEEACH']
    df['COUNTRY']  = df['COUNTRY'].str.strip().str.upper()
    df['DEALSIZE'] = df['DEALSIZE'].str.strip().str.title()
    logging.info("Added YEAR, MONTH, REVENUE columns")

    logging.info(f"Transform done. Final shape: {df.shape}")
    return df

def load(df):
    df.to_csv("output/sales_clean.csv", index=False)
    logging.info("Saved: output/sales_clean.csv")

    conn = sqlite3.connect("output/sales.db")
    df.to_sql("sales", conn, if_exists="replace", index=False)
    conn.close()
    logging.info("Saved: output/sales.db (table: sales)")

    conn = sqlite3.connect("output/sales.db")
    count = conn.execute("SELECT COUNT(*) FROM sales").fetchone()[0]
    top = conn.execute("""
        SELECT COUNTRY, ROUND(SUM(SALES), 2) AS total_sales
        FROM sales
        GROUP BY COUNTRY
        ORDER BY total_sales DESC
        LIMIT 5
    """).fetchall()
    conn.close()

    logging.info(f"Rows in DB: {count}")
    print("\n--- TOP 5 COUNTRIES BY SALES ---")
    for row in top:
        print(f"  {row[0]:<15} ${row[1]:>10,.2f}")

def run():
    start = datetime.now()
    logging.info("=== Pipeline started ===")

    df = extract("data/sales_data_sample.csv")
    df = transform(df)
    load(df)

    duration = (datetime.now() - start).total_seconds()
    logging.info(f"=== Pipeline completed in {duration:.2f}s ===")

if __name__ == "__main__":
    run()
"""
This script is used to load the cleaned data into a SQLite database.

"""
import pandas as pd

from wikipedia.src.sqllite.sqllite_engine import SqlLiteEngine


# Function to upload CSV to SQLite sqllite in chunks
def upload_csv_to_sqlite(file_path="../../data/clean/train_cleaned.csv", chunk_size=1000):
    engine = SqlLiteEngine.get_engine()

    table_name = 'page_visits'

    # Read CSV file in chunks
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        chunk.to_sql(table_name, engine, if_exists='append', index=False)


import csv
from datetime import datetime
from model import Visits, Key
import pandas as pd
from sqlalchemy import create_engine


# Function to load data from CSV to the 'page_visits' table
def load_page_visits_from_csv(csv_file, session):
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        #reader = csv.DictReader(csvfile)
        reader = pd.read_csv(csv_file)
        reader.to_sql()
        for row in reader:
            visit = Visits(
                Page=row['Page'],
                Date=datetime.strptime(row['Date'], '%Y-%m-%d').date(),
                Visits=float(row['Visits'])
            )
            session.add(visit)
        session.commit()

# Function to load data from CSV to the 'key' table
def load_keys_from_csv(csv_file, session):
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            key_entry = Key(
                id=row['id'],
                Page=row['Page']
            )
            session.add(key_entry)
        session.commit()


def create_sqlite_engine():
    engine = create_engine('sqlite:///wikipedia.db')
    return engine
# Function to upload CSV to SQLite database in chunks
def upload_csv_to_sqlite(file_path, chunk_size=1000):
    engine = create_sqlite_engine()
    conn = engine.connect()
    table_name = 'page_visits'

    # Read CSV file in chunks
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        chunk.to_sql(table_name, conn, if_exists='append', index=False)

    conn.close()

def main():
    file_path = "../data/clean/train_1_cleaned.csv"
    upload_csv_to_sqlite(file_path)

# if _name_ == "_main_":
main()

def download_data_from_sqlite(select_statement, file_path_to_save='../data/clean/cleaned_data.csv'):
    engine = create_engine('sqlite:///wikipedia.db')

    # Use pandas to execute the dummy select statement and read the data into a DataFrame
    df = pd.read_sql_query(select_statement, engine)

    # Save the DataFrame to a CSV file
    df.to_csv(file_path_to_save, index=False)

    print(f"Data downloaded and saved to {file_path_to_save}")

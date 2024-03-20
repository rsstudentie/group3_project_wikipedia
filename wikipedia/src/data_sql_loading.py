"""
File to load the data from csv to sql and create the appropriate table
"""
import loadsql

# def main():
#     file_path = "../data/clean/train_1_cleaned.csv"
#     loadsql.upload_csv_to_sqlite(file_path)
#
# # if _name_ == "_main_":
# main()

# """
# File to load the data from csv to sql and create the appropriate table
# """
# import pandas as pd
# from sqlalchemy import create_engine, Column, Integer, String, Date, Float, text
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# import loadsql as load
#
# engine = create_engine('sqlite:///..database/wikipedia.db')
#
# # Session = sessionmaker(bind=engine)
# # session = Session()
#
# #load.load_page_visits_from_csv('../data/clean/train_1_cleaned.csv', session)
# #load.load_keys_from_csv('../data/raw/key_1.csv', session)
#
#
# SessionLocal = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=engine,
# )
#
# df = pd.read_csv('../data/clean/train_1_cleaned.csv')
# df.head()
#
# with SessionLocal() as session:
#     df.to_sql('page_visits', con=engine, if_exists='replace', index=False)
#     result = pd.DataFrame(session.execute(text("SELECT * FROM page_visits")))
#
# result.head()
#
#
# session.close()

import pandas as pd
from sqlalchemy import create_engine

# Function to create SQLite engine
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
#
# def main():
#     file_path = "../data/clean/train_1_cleaned.csv"
#     upload_csv_to_sqlite(file_path)
#

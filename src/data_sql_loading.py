"""
File to load the data from csv to sql and create the appropriate table
"""
import loadsql

def main():
    file_path = "../data/clean/train_1_cleaned.csv"
    loadsql.upload_csv_to_sqlite(file_path)

# if _name_ == "_main_":
main()


import csv
from sqlalchemy import Table
def load_csv_to_table(engine, csv_file_path, table: Table, skip_header=True):
    """
    Loads data from a CSV file into a specified table using the given database engine.

    :param engine: SQLAlchemy engine object connected to the database.
    :param csv_file_path: Path to the CSV file to be loaded.
    :param table: SQLAlchemy Table object where data will be inserted.
    :param skip_header: Boolean indicating if the first row (header) should be skipped.
    """
    with engine.connect() as connection:
        with open(csv_file_path, newline='') as csvfile:
            csvreader = csv.reader(csvfile)

            # Skip the header row if specified
            if skip_header:
                next(csvreader, None)

            # Insert data into the table
            for row in csvreader:
                # Construct the insert statement dynamically based on the CSV row and table columns
                insert_stmt = table.insert().values({column.name: value for column, value in zip(table.columns, row)})
                connection.execute(insert_stmt)
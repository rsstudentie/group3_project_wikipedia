import csv

def transpose_csv(input_csv_path, output_csv_path, encoding='utf-8'):
    """
    Reads a CSV file using the specified encoding, transposes its rows and columns,
    and writes the transposed data to a new CSV file.

    :param input_csv_path: Path to the input CSV file.
    :param output_csv_path: Path to the output CSV file where the transposed data will be written.
    :param encoding: Encoding to use for reading the input CSV file. Defaults to 'utf-8'.
    """
    with open(input_csv_path, newline='', encoding=encoding) as input_file:
        reader = csv.reader(input_file)
        data = [row for row in reader]

    transposed_data = zip(*data)

    with open(output_csv_path, 'w', newline='', encoding=encoding) as output_file:
        writer = csv.writer(output_file)
        writer.writerows(transposed_data)





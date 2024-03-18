import os
from kaggle.api.kaggle_api_extended import KaggleApi
from zipfile import ZipFile

#
# def download_and_unzip_kaggle_dataset(dataset, path_to_save='../data/zip/'):
#     """
#     Downloads and unzips a Kaggle dataset into the specified directory.
#
#     Parameters:
#     - dataset (str): The Kaggle dataset path, e.g. 'competitions/web-traffic-time-series-forecasting'
#     - path_to_save (str): Local path where to save and unzip the dataset. Defaults to the current directory.
#
#     Requires:
#     - A Kaggle account
#     - A Kaggle API token (kaggle.json) placed in the location ~/.kaggle/kaggle.json or passed via environment variable
#
#     Example usage:
    #     download_and_unzip_kaggle_dataset('competitions/web-traffic-time-series-forecasting', './data')
#     """
#
#     # Authenticate with the Kaggle API
#     api = KaggleApi()
#     api.authenticate()
#
#     # Download the dataset (This will download all files in the dataset)
#     api.competition_download_files(dataset, path=path_to_save)
#
#     # Find the downloaded zip file and unzip it
#     zip_files = [f for f in os.listdir(path_to_save) if f.endswith('.zip')]
#     for zip_file in zip_files:
#         zip_path = os.path.join(path_to_save, zip_file)
#         with ZipFile(zip_path, 'r') as zip_ref:
#             zip_ref.extractall(path_to_save)
#         print(f"Unzipped file: {zip_path}")
#
#         # Optionally, remove the zip file after extraction
#         os.remove(zip_path)
#         print(f"Removed zip file: {zip_path}")
#
# # Example of calling the function (you need to replace 'path_to_save' with your path):
# # download_and_unzip_kaggle_dataset('competitions/web-traffic-time-series-forecasting', './data')


def download_and_unzip_kaggle_data(competition, destination, kaggle_json_path):
    # Set the environment variable for the Kaggle configuration directory
    os.environ['KAGGLE_CONFIG_DIR'] = os.path.dirname(kaggle_json_path)

    # Initialize Kaggle API
    api = KaggleApi()

    # Authenticate with the Kaggle API
    api.authenticate()

    # Download data for the specified competition
    api.competition_download_files(competition, path=destination)

    # Find the downloaded zip file
    zip_files = [f for f in os.listdir(destination) if f.endswith('.zip')]
    if not zip_files:
        print("No zip files found.")
        return

    # Unzip the downloaded files
    zip_file = os.path.join(destination, zip_files[0])
    with ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(destination)

    # Remove the zip file after extraction
    os.remove(zip_file)
    print("Data downloaded and extracted successfully.")



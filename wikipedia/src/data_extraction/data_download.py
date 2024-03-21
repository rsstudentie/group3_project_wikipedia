import os
from zipfile import ZipFile
from kaggle.api.kaggle_api_extended import KaggleApi


def download_and_unzip_data():
    """
    Downloads and extracts the data from Kaggle

    :param kaggle_json_path: str : The path to the kaggle.json file
    :return: None
    """

    # Set up the Kaggle API
    api = KaggleApi()

    # Authenticate using the provided kaggle.json file
    api.authenticate()

    # Define the competition name
    competition_name = "web-traffic-time-series-forecasting"

    # Define the directory to save the downloaded data
    data_dir = "../../../data"

    # Create the directory if it doesn't exist
    os.makedirs(data_dir, exist_ok=True)

    try:
        # Download the competition data
        api.competition_download_files(competition_name, path=data_dir)

        # Extract the zip file
        with ZipFile(os.path.join(data_dir, competition_name + ".zip"), 'r') as zip_ref:
            zip_ref.extractall(data_dir)

        print("Data downloaded and extracted successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def download_data():
    """
    Downloads the data from Kaggle

    :param kaggle_json_path: str : The path to the kaggle.json file
    :return: None
    """

    # Set up the Kaggle API
    api = KaggleApi()

    # Authenticate using the provided kaggle.json file
    api.authenticate()

    # Define the competition name
    competition_name = "web-traffic-time-series-forecasting"

    # Define the directory to save the downloaded data
    data_dir = "../../../data/raw/"

    # Create the directory if it doesn't exist
    os.makedirs(data_dir, exist_ok=True)

    try:
        # Download the competition data
        api.competition_download_files(competition_name, path=data_dir)

        print("Data downloaded successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def unzip_data():
    """
    Extracts the data from the downloaded zip file

    :return: None
    """

    # Define the competition name
    competition_name = "web-traffic-time-series-forecasting"

    # Define the directory to save the downloaded data
    data_dir = "../../../data/raw/"

    try:
        # Extract the zip file
        with ZipFile(os.path.join(data_dir, competition_name + ".zip"), 'r') as zip_ref:
            zip_ref.extractall(data_dir)

        print("Data extracted successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

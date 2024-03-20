"""
Data Cleaning for the datasets of Wikpedia timeseries
    Returns a _cleaned.csv file for further analysis
"""

import pandas as pd


def clean_raw_data():
    """
    Function to clean the raw data and save it to a new csv file

    :return: train_data: cleaned data in a pandas dataframe
    """

    # Path to the raw data
    data_path = "../../data/raw/train_1.csv"

    # Loading the csv file into a dataframe
    df = pd.read_csv(data_path)

    # Fill missing values
    df = df.fillna(0)

    # Melting the data to reduce number of columns (previously 551)
    train_data = pd.melt(df, id_vars=['Page'], var_name='Date', value_name='Visits')

    # Saving the cleaned data to a new csv file
    train_data.to_csv('../../data/clean/train_cleaned.csv', index=True)

    return train_data


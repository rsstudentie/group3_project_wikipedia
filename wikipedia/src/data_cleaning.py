"""
Data Cleaning for the datasets of Wikpedia timeseries
    Returns a _cleaned.csv file for further analysis
"""

import pandas as pd

# Loading the csv file into a dataframe
## Uncomment the file you need
data_path = "../data/raw/train_1.csv"
# data_path = "../data/raw/train_2.csv"
# data_path = "../data/raw/key_1.csv"
# data_path = "../data/raw/key_2.csv"

df = pd.read_csv(data_path)
#df.head()

# Fill missing values
df = df.fillna(0)

# Melting the data to reduce number of columns (previously 551)
train_data = pd.melt(df,id_vars=['Page'],var_name='Date',value_name='Visits')
# train_data.head()
# train_data.shape
# (79784650, 3)

train_data = train_data.sample

# Uncomment this to use a smaller sample of data
#train_data = train_data.sample(frac=0.2)

# If csv file used is train_1
train_data.to_csv('../data/clean/train_1_cleaned.csv', index=True)
# # If csv file used is train_2
# train_data.to_csv('../data/clean/train_2_cleaned.csv', index=True)
# # If csv file used is key_1
# train_data.to_csv('../data/clean/key_1_cleaned.csv', index=True)
# # If csv file used is key_2
# train_data.to_csv('../data/clean/key_2_cleaned.csv', index=True)


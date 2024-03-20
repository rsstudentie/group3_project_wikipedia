"""
Data Visualization for the datasets of Wikpedia timeseries
    Works on the XXXXX file created in the Wikipedia_DataVisualization.py

    There are anomalies in the period between 07/2016 and 09/2016
    using isolation forest we will remove anomalies
"""

import pandas as pd
from sklearn.ensemble import RandomForestRegressor, IsolationForest
import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect('wikitop100.db')
query = 'SELECT Date, Visits FROM page_visits'
page_visits_df = pd.read_sql_query(query, conn)
conn.close()

top_page_df = page_visits_df.set_index('Date')

print(top_page_df.head())

# Setting up the Isolation Forest model and fitting it to the DF
isolation_forest_model = IsolationForest(contamination=0.05)
isolation_forest_model.fit(top_page_df)
top_page_df['anomaly'] = isolation_forest_model.predict(top_page_df)

# Plotting the data to better visualize anomalies
fig, ax = plt.subplots(figsize=(45,5))
anomaly_df = top_page_df.loc[top_page_df['anomaly'] == -1].copy()
ax.plot(top_page_df.index,top_page_df['Visits'],color='blue', label = 'Normal')
plt.scatter(anomaly_df.index,anomaly_df['Visits'],color='red',s=100,label = 'Anomaly')
plt.legend()
plt.show()

# Removing anomalies from the data
top_page_df['new_visits'] = top_page_df.apply(lambda row: row.Visits if row.anomaly == 1 else None, axis='columns')
plt.figure(figsize=(25,4))
plt.plot(top_page_df.index,top_page_df.new_visits)

# Filling missing data with rolling mean
top_page_df = top_page_df.assign(rolling_mean=top_page_df.new_visits.fillna(top_page_df.new_visits.rolling(30,min_periods=1).mean()))

# Plotting the Data after removing anomalies
plt.figure(figsize=(25,4))
plt.plot(top_page_df.index,top_page_df.rolling_mean)
plt.title('Data after removing anomalies')
plt.xlabel('Date')
plt.ylabel('Views (in millions)')
plt.show()

# top_page_df.drop(columns=['Visits','anomaly','new_visits'], inplace=True)
# top_page_df = top_page_df.rename(columns={'rolling_mean':'Views'})

print(top_page_df.head())

#top_page_df.to_sql('no_anomaly_visits', con=sqlite3.connect('wikitop100.db'), if_exists='replace', index=False)


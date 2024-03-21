"""
Data Visualization for the datasets of Wikipedia timeseries
Downloads data from SQLite and through pandas reads it into a DataFrame
the download function presents a select_statement argument in which
a desired select statement can be inputted.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# import def_language as language
import sqlite3

from wikipedia.src.analytics import language
from wikipedia.src.sqllite.sqllite_engine import SqlLiteEngine
from sqlalchemy import text

""" We need to import the data from the SQL sqllite"""

def plot_avg_views_per_day():
    session = SqlLiteEngine().get_session()
    with session as session:
        result = session.execute(text('SELECT * FROM page_visits'))
        train_data = pd.DataFrame(result)

    # Transforming the Date column to a datetime format
    train_data['Date'] = pd.DatetimeIndex(train_data['Date'])

    # Calculate the average number of views per day
    temp = train_data.groupby('Date')['Visits'].mean()

    # Set up the plot
    plt.figure(figsize=(15, 4))
    plt.xlabel('Date', fontsize=8)
    plt.ylabel('Avg views', fontsize=8)
    plt.title('Average number of views per day', fontsize=12)

    # Plot the average views per day

    # # Set up the ticks
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)

    # Show legend
    plt.legend()

    # Adjust layout and show the plot
    plt.plot(temp, label='Visits')
    plt.tight_layout()
    plt.show()

    return plt

def plot_median_views_per_day():
    session = SqlLiteEngine().get_session()
    with session as session:
        result = session.execute(text('SELECT * FROM page_visits'))
        train_data = pd.DataFrame(result)

    # Calculate the median number of views per day
    temp = train_data.groupby('Date')['Visits'].median()

    # Set up the plot
    plt.figure(figsize=(15, 4))
    plt.xlabel('Date', fontsize=8)
    plt.ylabel('Median views', fontsize=8)
    plt.title('Median number of views per day', fontsize=8)

    # Plot the median views per day

    plt.legend()
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.tight_layout()

    plt.plot(temp, label='Visits')
    plt.show()

    return plt

def extract_date_components():
    """
    Extracts year, month, and day from a date column in a DataFrame and creates new columns for each.

    Parameters:

    """

    session = SqlLiteEngine().get_session()
    with session as session:
        result = session.execute(text('SELECT * FROM page_visits'))
        df = pd.DataFrame(result)


    # Ensure the date column is in datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    # Create new columns for year, month, and day
    df['year'] = df['Date'].dt.year
    df['month'] = df['Date'].dt.month
    df['day'] = df['Date'].dt.day

    return df

# Plotting web traffic over days of month using heatmap
def plot_web_traffic_over_days_of_month():
    session = SqlLiteEngine().get_session()
    with session as session:
        result = session.execute(text('SELECT * FROM page_visits'))
        train_data = pd.DataFrame(result)

    train_data = extract_date_components()

    # Creating new column and replacing month with encoded value
    train_data['month_num'] = train_data['month']
    train_data['month'].replace('1', '1 - January', inplace=True)
    train_data['month'].replace('2', '2 - February', inplace=True)
    train_data['month'].replace('3', '3 - March', inplace=True)
    train_data['month'].replace('4', '4 - April', inplace=True)
    train_data['month'].replace('5', '5 - May', inplace=True)
    train_data['month'].replace('6', '6 - June', inplace=True)
    train_data['month'].replace('7', '7 - July', inplace=True)
    train_data['month'].replace('8', '8 - August', inplace=True)
    train_data['month'].replace('9', '9 - September', inplace=True)
    train_data['month'].replace('10', '10 - October', inplace=True)
    train_data['month'].replace('11', '11 - November', inplace=True)
    train_data['month'].replace('12', '12 - December', inplace=True)

    # Creating a new column weekday and applying lambda function to extract from date column
    train_data['weekday'] = train_data['Date'].apply(lambda x: x.weekday())

    # Creating new column and encoding weekday
    train_data['weekday#'] = train_data['weekday']
    train_data['weekday'].replace(0, '01 - Monday', inplace=True)
    train_data['weekday'].replace(1, '02 - Tuesday', inplace=True)
    train_data['weekday'].replace(2, '03 - Wednesday', inplace=True)
    train_data['weekday'].replace(3, '04 - Thursday', inplace=True)
    train_data['weekday'].replace(4, '05 - Friday', inplace=True)
    train_data['weekday'].replace(5, '06 - Saturday', inplace=True)
    train_data['weekday'].replace(6, '07 - Sunday', inplace=True)

    # train_data.head()

    # Creating copy of the dataframe and grouping by month and weekday and looking at the mean of the visits
    train_group = train_data.groupby(["month", "weekday"])['Visits'].mean().reset_index()
    train_group = train_group.pivot(index='weekday', columns='month', values='Visits')
    train_group.sort_index(inplace=True)

    sns.set(font_scale=3.5)
    f, ax = plt.subplots(figsize=(60, 40))
    sns.heatmap(train_group, annot=False, ax=ax, fmt="d", linewidths=2)
    plt.title('Web Traffic of various months(9-12) across weekdays')
    plt.show()

    return plt

###
# # Dropping columns previously created for new visualization
# cols_to_drop = ['year', 'month', 'day', 'month_num', 'weekday', 'weekday', 'weekday#']
# train_data.drop(cols_to_drop, axis=1, inplace=True)
# train_data

def top_pages():
    """
    Function to identify the top 5 pages with the maximum number of views

    :return: top_pages_list: list of top 5 pages with maximum number of views
    """
    session = SqlLiteEngine().get_session()
    with session as session:
        result = session.execute(text('SELECT * FROM page_visits'))
        train_data = pd.DataFrame(result)

    # Top 5 pages with maximum number of views
    top_pages = train_data.groupby('Page')['Visits'].sum().reset_index()
    top_pages_list = top_pages.nlargest(5, 'Visits')['Page'].tolist()

    return top_pages_list

# Detecting page language from URL code
def detect_language():
    """
    Function to detect the language of the Wikipedia page

    :return: temp1: DataFrame with Wikipedia page language and language code
    """
    session = SqlLiteEngine().get_session()
    with session as session:
        result = session.execute(text('SELECT * FROM page_visits'))
        train_data = pd.DataFrame(result)

    # Detecting the language of the Wikipedia page
    temp1 = train_data
    temp1['Wikipedia_page'] = temp1.Page.apply(language.detect_language)

    # Creating a new column for detecting the language from the page title
    temp1['Page_language'] = temp1.Wikipedia_page.apply(language.lang_code)

    return temp1


###

# Time-series of page with maximum views
def time_series_of_page_with_max_views():
    """
    Function to plot the time-series of the page with the maximum number of views

    :return: top_page_df: DataFrame with time-series of the page with the maximum number of views
    """
    top_pages_list = top_pages()
    temp1 = detect_language()

    # Time-series of page with maximum views
    top_page_df = temp1[temp1.Page == top_pages_list[0]]
    top_page_df['Visits'] = top_page_df['Visits'].div(1000000).round(2)

    # Drop columns not used in next plots
    top_page_df.drop(['Page', 'Wikipedia_page', 'Page_language'], axis=1, inplace=True)

    # Resetting index
    top_page_df.reset_index(inplace=False)

    top_page_df.plot()
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.show()

    return plt

# run all the functions
# plot_avg_views_per_day()
# plot_median_views_per_day()
# plot_web_traffic_over_days_of_month()
# time_series_of_page_with_max_views()
# detect_language()
# top_pages()
# extract_date_components()

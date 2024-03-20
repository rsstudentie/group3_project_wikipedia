"""
File that plots comparison between mobile and desktop accesses
"""

import pandas as pd
import matplotlib.pyplot as plt

from wikipedia.src.sqllite.sqllite_engine import SqlLiteEngine


def analyze_time_series():
    session = SqlLiteEngine().get_session()
    with session as session:
        result = session.execute('SELECT * FROM page_visits')
        df = pd.DataFrame(result)

    # Convert 'Date' to datetime if it's not already
    df['Date'] = pd.to_datetime(df['Date'])

    # Filter data for mobile and desktop, and aggregate by date
    mobile_data = df[df['Page'].str.contains('mobile')].groupby('Date')['Visits'].sum()
    desktop_data = df[df['Page'].str.contains('desktop')].groupby('Date')['Visits'].sum()

    # Plotting the time series
    plt.figure(figsize=(14, 7))
    plt.plot(mobile_data.index, mobile_data.values, label='Mobile')
    plt.plot(desktop_data.index, desktop_data.values, label='Desktop')
    plt.xlabel('Date')
    plt.ylabel('Number of Visits')
    plt.title('Mobile vs Desktop Visits Over Time')
    plt.legend()
    plt.tight_layout()
    plt.show()

    return plt


def compare_visits_bar_chart():
    session = SqlLiteEngine().get_session()
    with session as session:
        result = session.execute('SELECT * FROM page_visits')
        df = pd.DataFrame(result)

    # Aggregate total visits by type
    total_mobile_visits = df[df['Page'].str.contains('mobile')]['Visits'].sum()
    total_desktop_visits = df[df['Page'].str.contains('desktop')]['Visits'].sum()

    # Data for plotting
    labels = ['Mobile', 'Desktop']
    visits = [total_mobile_visits, total_desktop_visits]

    # Plotting the bar chart
    plt.figure(figsize=(8, 6))
    plt.bar(labels, visits, color=['blue', 'orange'])
    plt.xlabel('Type of Access')
    plt.ylabel('Total Number of Visits')
    plt.title('Total Mobile Visits vs Desktop Visits')
    plt.tight_layout()
    plt.show()

    return plt

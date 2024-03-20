import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

conn = sqlite3.connect('wikitop100.db')
query = 'SELECT * FROM page_visits'
df = pd.read_sql_query(query, conn)
conn.close()


def plot_time_series(df, page_to_plot):
    single_page_df = df[df['Page'] == page_to_plot]
    plt.figure(figsize=(14, 7))
    plt.plot(single_page_df['Date'], single_page_df['Visits'], label=page_to_plot)
    plt.xlabel('Date')
    plt.ylabel('Visits')
    plt.title(f'Visits Over Time for {page_to_plot}')
    plt.legend()
    plt.tight_layout()
    plt.show()
    return plt


def plot_bar_chart(df):
    page_visits_total = df.groupby('Page')['Visits'].sum().sort_values(ascending=False)[:10]
    plt.figure(figsize=(12, 8))
    page_visits_total.plot(kind='bar')
    plt.xlabel('Page')
    plt.ylabel('Total Visits')
    plt.title('Top Pages by Total Visits')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
    return plt


def visualize_data(df):
    # Assuming the 'Date' column is already in datetime format

    # Plotting the first page's time series as an example
    first_page = df['Page'].unique()[0]
    plot_time_series(df, first_page)

    # Plotting bar chart for top pages
    plot_bar_chart(df)

# Now to call the main function, ensure you pass the DataFrame after loading your data:
# visualize_data(your_dataframe)
visualize_data(df)
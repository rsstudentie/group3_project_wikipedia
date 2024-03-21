from wikipedia.src.sqllite.sqllite_engine import SqlLiteEngine
from wikipedia.src.analytics.devices import compare_visits_bar_chart, analyze_time_series
from wikipedia.src.analytics.random_forest import random_forest
from wikipedia.src.data_extraction.data_cleaning import clean_raw_data
from wikipedia.src.data_extraction.data_sampling import sample_data
from wikipedia.src.data_extraction.data_sql_loading import upload_csv_to_sqlite
from wikipedia.src.data_extraction.data_download import download_and_unzip_data
from src.visualization.data_visualization import plot_avg_views_per_day, plot_median_views_per_day, \
    plot_web_traffic_over_days_of_month, time_series_of_page_with_max_views
from wikipedia.src.analytics.anomaly_detection import anamoly_detection
from sqlalchemy import text

import typer

import streamlit as st

app = typer.Typer()


@app.command()
def initdb():
    init_database()


@app.command()
def kaggledownload():
    download_and_unzip_data()
    clean_raw_data()


@app.command()
def sampledata():
    sample_data()
    upload_csv_to_sqlite()


@app.command()
def getrows(db: str):
    if db == 'working':
        db_engine = SqlLiteEngine(db="wikipedia")
    elif db == 'complete':
        db_engine = SqlLiteEngine(db="wikipedia_complete")

    session = SqlLiteEngine.get_session()
    with session as session:
        result = session.execute(text('SELECT count(*) FROM page_visits'))
        print(result)


def init_database():
    """"
    Initialize the database
    """

    # Initiate the SqlLiteEngine with a specific database name and root folder
    db_engine = SqlLiteEngine(db="wikipedia")
    print("Database Initialized")


# Call visualization functions from each file in a seperate functions


# visualize_data(df)


def init_projecct():
    init_database()


def main():
    st.sidebar.title("Navigation")

    if st.sidebar.button("Basic Analysis"):
        st.title("Average and Median Views per Day")
        t1 = plot_avg_views_per_day()
        st.pyplot(t1)

        t2 = plot_median_views_per_day()
        st.pyplot(t2)

        st.title("Web Traffic Over Days of Month")
        t3 = plot_web_traffic_over_days_of_month()
        st.pyplot(t3)

        t4 = time_series_of_page_with_max_views()
        st.pyplot(t4)

    if st.sidebar.button("Anamoaly Detection"):
        st.title("Anamolies in the Data")
        t1 = anamoly_detection()
        st.pyplot(t1)

        # Add your bar chart code here

    if st.sidebar.button("Random Forrest"):
        st.title("Anamolies in the Data")
        plt, mae, rmse, r_squared, mape = random_forest()

        st.pyplot(plt)

        st.text(f'Mean Absolute Error: {mae}')
        st.text(f'Root Mean Squared Error: {rmse}')
        st.text(f'R-squared: {r_squared}')
        st.text(f'Mean Absolute Percentage Error (MAPE): {mape}%')

    if st.sidebar.button("Device Analysis"):
        st.title("Device Analysis")
        t1 = compare_visits_bar_chart()
        t2 = analyze_time_series()

        st.pyplot(t1)
        st.pyplot(t2)

        # Add your bar chart code here

    # Button to call function from different module
    if st.sidebar.button("New Analysis"):
        st.title("Device Analysis")
        t1 = compare_visits_bar_chart()
        t2 = analyze_time_series()

        st.pyplot(t1)
        st.pyplot(t2)

    # if st.button("Start New Analysis"):

    # print(f'Mean Absolute Error: {mae}')
    # print(f'Root Mean Squared Error: {rmse}')
    # print(f'R-squared: {r_squared}')
    # print(f'Mean Absolute Percentage Error (MAPE): {mape}%')


if __name__ == "__main__":
    init_projecct()
    main()

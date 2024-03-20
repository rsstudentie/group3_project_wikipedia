from src.sqllite.sqllite_engine import SqlLiteEngine
# from src.data_extraction.data_download import download_and_unzip_data

from wikipedia.src.visualization.data_visualization import plot_avg_views_per_day, \
    plot_median_views_per_day, plot_web_traffic_over_days_of_month, time_series_of_page_with_max_views


def init_database():
    """"
    Initialize the database
    """

    # Initiate the SqlLiteEngine with a specific database name and root folder
    db_engine = SqlLiteEngine(db="wikipedia")
    print("Database Initialized")


def init_projecct():
    init_database()

    # file_path = "../data/clean/train_1_cleaned.csv"
    # upload_csv_to_sqlite(file_path)
    # download_and_unzip_data()

    # anamoly_detection()

    # timeseries()

    # data_visualization()

    # plt, mae, rmse, r_squared, mape = random_forest()
    # plt.show()
    #
    # print(f'Mean Absolute Error: {mae}')
    # print(f'Root Mean Squared Error: {rmse}')
    # print(f'R-squared: {r_squared}')
    # print(f'Mean Absolute Percentage Error (MAPE): {mape}%')


    # Call the migrate_data function to execute the migration
    # migrate_data()
    # Run this wherever using the database
    # engine = SqlLiteEngine.get_engine()
    # session = SqlLiteEngine().get_session()
    # with session as session:
    #     session.execute(#####)

    plot_avg_views_per_day()
    plot_median_views_per_day()
    plot_web_traffic_over_days_of_month()
    time_series_of_page_with_max_views()
    # detect_language()
    # top_pages()
    # extract_date_components()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("Project Initialized")
    init_projecct()

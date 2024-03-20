from src.sqllite.sqllite_engine import SqlLiteEngine
from wikipedia.src.analytics.devices import compare_visits_bar_chart, analyze_time_series
from wikipedia.src.analytics.random_forest import random_forest
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


# Call visualization functions from each file in a seperate functions


def init_projecct():
    init_database()

    plt, mae, rmse, r_squared, mape = random_forest()
    plt.show()

    print(f'Mean Absolute Error: {mae}')
    print(f'Root Mean Squared Error: {rmse}')
    print(f'R-squared: {r_squared}')
    print(f'Mean Absolute Percentage Error (MAPE): {mape}%')


    # Call the migrate_data function to execute the migration
    # migrate_data()


    plot_avg_views_per_day()
    plot_median_views_per_day()
    plot_web_traffic_over_days_of_month()
    time_series_of_page_with_max_views()

    compare_visits_bar_chart()
    analyze_time_series()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("Project Initialized")
    init_projecct()

from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import rcParams
import numpy as np
# import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from wikipedia.src.sqllite.sqllite_engine import SqlLiteEngine


def random_forest():
    # Initiating engine
    session = SqlLiteEngine().get_session()
    with session as session:
        result = session.execute('SELECT * FROM page_visits')
        df = pd.DataFrame(result)

    sample_pages = df['Page'].drop_duplicates().sample(n=5, random_state=1201).values

    rcParams['font.family'] = "Arial Unicode MS"

    df['Date'] = pd.to_datetime(df['Date'])

    plt.figure(figsize=(15, 10))

    # Set the locator for the x-axis to pick fewer date ticks (e.g., monthly)
    locator = mdates.MonthLocator()  # Locator can be adjusted to YearLocator, WeekLocator, etc.
    formatter = mdates.DateFormatter('%Y-%m')  # Adjust the format as needed

    for page in sample_pages:
        page_data = df[df['Page'] == page]
        plt.plot(page_data['Date'], page_data['Visits'], label=page)

    plt.title('Web Traffic Time Series for Sample Articles')
    plt.xlabel('Date')
    plt.ylabel('Visits')
    plt.legend()

    # Set major and minor locators and formatters
    ax = plt.gca()
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

    plt.xticks(rotation=45)
    plt.tight_layout()
    # plt.show()

    df.sort_values(by=['Page', 'Date'], inplace=True)

    for i in range(1, 8):  # 7 day lag
        df[f'lag_{i}'] = df.groupby('Page')['Visits'].transform(lambda x: x.shift(i))

    df_clean = df.dropna(subset=[f'lag_{i}' for i in range(1, 8)])
    df_clean = df_clean.copy()
    df_clean['Date'] = pd.to_datetime(df_clean['Date'])

    split_date = df_clean['Date'].max() - pd.Timedelta(days=30)

    # Splitting the dataset
    train = df_clean[df_clean['Date'] <= split_date]
    test = df_clean[df_clean['Date'] > split_date]

    # Preparing features (X) and target (y) for both training and testing sets
    X_train = train.drop(['Page', 'Date', 'Visits'], axis=1)
    y_train = train['Visits']
    X_test = test.drop(['Page', 'Date', 'Visits'], axis=1)
    y_test = test['Visits']

    rfr = RandomForestRegressor(n_estimators=100, random_state=1201)
    rfr.fit(X_train, y_train)

    predictions = rfr.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions, squared=False)
    r_squared = r2_score(y_test, predictions)
    mape = np.mean(np.abs((y_test - predictions) / y_test)) * 100

    print(f'Mean Absolute Error: {mae}')
    print(f'Root Mean Squared Error: {rmse}')
    print(f'R-squared: {r_squared}')
    print(f'Mean Absolute Percentage Error (MAPE): {mape}%')

    return plt, mae, rmse, r_squared, mape
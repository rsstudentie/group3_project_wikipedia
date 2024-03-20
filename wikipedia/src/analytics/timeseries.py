"""
Plotting TimeSeries analysis for Wikipedia
    Working on the XXXX file from the Wikipedia_AnomalyDetection.py
"""

import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics import tsaplots
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.api import SimpleExpSmoothing
from pmdarima import auto_arima
import sqlite3

from wikipedia.src.sqllite.sqllite_engine import SqlLiteEngine

def timeseries():
    session = SqlLiteEngine().get_session()
    with session as session:
        result = session.execute('SELECT Date, Visits FROM page_visits')
        page_visits_df = pd.DataFrame(result)

    top_page_df = page_visits_df

    print(top_page_df.head())

    """
    ADF Test
    First element of output is the test statistic.
    Test statistic shows how likely the data is stationary
    Second element indicates the p-value.
    If p-value is >0.05, reject null hypothesis or else not,
    The null hypothesis is that data is not stationary.
    """

    # Plotting the ACF for visual interpretation
    fig = tsaplots.plot_acf(top_page_df['Visits'], lags=60)
    plt.show()

    test = adfuller(top_page_df['Visits'])
    print(test)
    # Data is not stationary for the p-value

    # Applying one difference to the data to make it stationary
    top_page_stationary_df = top_page_df['Visits'].diff().dropna()
    ax = top_page_stationary_df.plot()

    # ADF test on stationary data
    test2 = adfuller(top_page_stationary_df)
    print(test2)


    ## Data is stationary

    # top_page_df
    # Preparing data for modelling
    top_page_df = top_page_df.sort_index()
    top_page_df.index = pd.to_datetime(top_page_df.index)

    # Manually slicing data based on date
    train = top_page_df[:'2016-09']
    test = top_page_df['2016-10':]

    # ACF plot
    fig = tsaplots.plot_acf(train['Visits'], lags=30)
    plt.show()

    # PACF plot
    fig = tsaplots.plot_pacf(train['Visits'], lags=30)
    plt.show()

    """

                ARMA Model

    """

    # Creating and Fitting ARMA models
    aic_bic_values = []
    for p in range(7):
        for q in range(7):
            try:
                model = SARIMAX(train, order=(p, 0, q))
                result = model.fit()
                aic_bic_values.append((p, q, result.aic, result.bic))
            except:
                continue

    # Sorting AIC and BIC values in ascending order for model selection
    aic_bic_df = pd.DataFrame(aic_bic_values, columns=['p', 'q', 'aic', 'bic'])
    aic_bic_df = aic_bic_df.sort_values(by=['aic', 'bic'])

    aic_bic_df.head()


    # Predicting using ARMA model
    # model = SARIMAX(train, order=(int(aic_bic_df.iloc[0]['p']), 0, int(aic_bic_df.iloc[0]['q'])))
    # result = model.fit()
    #
    # # import pickle
    # # with open('arma_model.pkl', 'wb') as f:
    # #     pickle.dump(model, f)
    #
    # # Forecasting the last 30 points
    # forecast = result.get_prediction(start=-30)
    # forecast_mean = forecast.predicted_mean
    # confidence_interval = forecast.conf_int()
    #
    # # Plotting the Prediction using ARMA
    # fig, ax = plt.subplots()
    # train[-30:].rename(columns={'Visits': 'actual value'}).plot(ax=ax)
    # forecast_mean.plot(ax=ax, label='prediction')
    # plt.fill_between(confidence_interval.index, \
    #                  confidence_interval['lower Views'], \
    #                  confidence_interval['upper Views'], \
    #                  color='pink', alpha=0.5)
    # plt.legend()
    # plt.show()
    #
    # # Plotting the Forecast using ARMA
    # forecast_values = result.get_forecast(steps=test.shape[0])
    # forecast_values_mean = forecast_values.predicted_mean
    # conf_interval = forecast_values.conf_int()
    #
    # arma_forecast_df = pd.DataFrame({'Date': test.index, 'Visits': forecast_values.predicted_mean,
    #                                  'lower_views': conf_interval['lower Views'].values,
    #                                  'upper_views': conf_interval['upper Views'].values})
    # arma_forecast_df = arma_forecast_df.set_index('Date')
    #
    # fig, ax = plt.subplots()
    # test.rename(columns={'Visits': 'Actual value'}).plot(ax=ax)
    # arma_forecast_df[['Visits']].rename(columns={'Visits': 'Forecast'}).plot(ax=ax, label='Forecast')
    # plt.fill_between(arma_forecast_df.index, \
    #                  arma_forecast_df.lower_views, \
    #                  arma_forecast_df.upper_views, \
    #                  color='pink', alpha=0.5)
    # plt.title('Forecasted number of views for the next 30 days')
    # plt.legend()
    # plt.show()
    #
    # # Calculating the mean squared difference of the forecasts
    # rmse_values = []
    # rmse_values.append(('ARMA', np.sqrt(np.mean(np.square(forecast_values_mean.values - test.Views.values)))))
    # print(rmse_values)
    #
    # # for date, (actual, forecast) in zip(test.index, zip(test['Views'].values, forecast_values_mean.values)):
    # #     print(f"Date: {date}, Actual: {actual}, Forecast: {forecast}")
    #
    # """
    #
    #             ARIMA Model
    #
    # """
    #
    # # Creating and Fitting ARIMA models
    # arima_aic_bic = []
    # for p in range(7):
    #     for q in range(7):
    #         try:
    #             arima_model = SARIMAX(train, order=(p, 1, q))
    #             arima_result = arima_model.fit()
    #             arima_aic_bic.append((p, q, arima_result.aic, arima_result.bic))
    #         except:
    #             continue
    #
    # arima_aic_bic_df = pd.DataFrame(arima_aic_bic, columns=['p', 'q', 'aic', 'bic'])
    # arima_aic_bic_df = arima_aic_bic_df.sort_values(by=['aic', 'bic'])
    #
    # # Predict using ARIMA
    # arima_model = SARIMAX(train, order=(int(aic_bic_df.iloc[0]['p']), 1, int(aic_bic_df.iloc[0]['q'])))
    # arima_result = arima_model.fit()
    # arima_forecast_mean = arima_result.get_prediction(steps=-30).predicted_mean
    #
    # # with open('arima_model.pkl', 'wb') as f:
    # #     pickle.dump(arima_model, f)
    #
    # # Plotting the diagnostics
    # # plt.figure(figsize=(24,4))
    # plt.figure(figsize=(15, 12), dpi=100)
    # arima_result.plot_diagnostics()  ##### ????
    # plt.show()
    #
    # arima_result.summary()
    #
    # # Plotting the prediction
    # fig, ax = plt.subplots()
    # train[-30:].rename(columns={'Visits': 'actual value'}).plot(ax=ax)
    # arima_forecast_mean[-30:].plot(ax=ax, label='prediction')
    # plt.legend()
    # plt.show()
    #
    # # Forecasting using ARIMA moidel
    # arima_forecast_values = arima_result.get_forecast(steps=test.shape[0])
    # arima_forecast_mean = arima_forecast_values.predicted_mean
    # arima_conf_interval = arima_forecast_values.conf_int()
    #
    # arima_forecast_df = pd.DataFrame({'Date': test.index, 'Visits': arima_forecast_values.predicted_mean,
    #                                   'lower_views': arima_conf_interval['lower Views'].values,
    #                                   'upper_views': arima_conf_interval['upper Views'].values})
    # arima_forecast_df = arima_forecast_df.set_index('Date')
    #
    # fig, ax = plt.subplots()
    # test.rename(columns={'Visits': 'Test'}).plot(ax=ax)
    # arima_forecast_df[['Visits']].rename(columns={'Visits': 'Forecast'}).plot(ax=ax)
    # plt.fill_between(arima_forecast_df.index, \
    #                  arima_forecast_df.lower_views, \
    #                  arima_forecast_df.upper_views, \
    #                  color='pink', alpha=0.5)
    # plt.title('Forecasted number of views for the next 30 days')
    # plt.legend()
    # plt.show()
    #
    # rmse_values.append(('ARIMA', np.sqrt(np.mean(np.square(arima_forecast_df.Views.values - test.Views.values)))))
    #
    # """
    #
    #         Exponential Smoothing Model
    #
    # """
    #
    # # Iniating the Smoothing model
    # exp_smoothing_model = SimpleExpSmoothing(train)
    # exp_smoothing_result = exp_smoothing_model.fit(smoothing_level=0.5, optimized=True)
    #
    # # Prediction using Exponential Smoothing model
    # exp_smoothing_prediction = exp_smoothing_result.predict(start=train[-30:-29].index[0], end=train[-1:].index[0])
    #
    # plt.figure(figsize=(25, 5))
    # plt.plot(train[-30:], label='Actual value')
    # plt.plot(exp_smoothing_prediction, label='Prediction')
    # plt.legend(loc='best')
    # plt.show()
    #
    # # plt.show()
    # # with open('exp_smoothing_model.pkl', 'wb') as f:
    # #     pickle.dump(exp_smoothing_model, f)
    #
    # # Forecasting using Exponential smoothing model
    # exp_smoothing_forecast = exp_smoothing_result.forecast(test.shape[0])
    # plt.figure(figsize=(25, 5))
    #
    # plt.plot(top_page_df)
    # plt.plot(exp_smoothing_forecast, label='Forecast')
    # plt.legend(loc='best')
    # plt.show()
    #
    # rmse_values.append(
    #     ('Exponential Smoothing', np.sqrt(np.mean(np.square(exp_smoothing_forecast.values - test.Views.values)))))
    #
    # """
    #
    #         Auto ARIMA model
    #
    # """
    #
    # # Initiating the model and fitting it on the data
    # auto_arima_model = auto_arima(train, start_p=2, max_p=7, start_q=2, max_q=7, m=1, stationary=False, trace=True,
    #                               seasonal=False, error_action='ignore', suppress_warnings=True)
    # auto_arima_model.fit(train)
    #
    # # Forecasting using auto ARIMA model
    # auto_arima_forecast = auto_arima_model.predict(n_periods=test.shape[0])
    # auto_arima_forecast = pd.DataFrame(auto_arima_forecast, index=test.index, columns=['Forecast'])
    #
    # plt.figure(figsize=(25, 6))
    # plt.plot(train, label='Train')
    # plt.plot(test, label='Test')
    # plt.plot(auto_arima_forecast, label='Forecast')
    # plt.legend()
    # plt.show()
    #
    # # with open('auto_arima_model.pkl', 'wb') as f:
    # #     pickle.dump(auto_arima_model, f)
    #
    # rmse_values.append(('Auto-arima', np.sqrt(np.mean(np.square(auto_arima_forecast.values - test.Views.values)))))
    #
    # """
    #
    #         Comparing RMSE Values
    #
    # """
    # # RMSE
    # rmse_df = pd.DataFrame(rmse_values, columns=['Model', 'RMSE_values']).sort_values('RMSE_values')
    #
    # for index, row in rmse_df.iterrows():
    #     print(f"The RMSE for the {row['Model']} model is: {row['RMSE_values']}")
    #
    # print(rmse_df)


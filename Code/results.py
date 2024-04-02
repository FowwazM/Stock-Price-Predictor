import numpy as np
import pandas as pd
from preprocessing import preprocess_data, forecast_data
from model import predict

def result(firm):
    # Check if firm has been provided by function caller
    if firm == '':
        firm = str(input("Please input the ticker of a firm on the S&P500: "))
    
    # Set forecasting time period
    forecast_timeperiod = 28

    # Import datasets and model results
    _, _, _, y_test, _, dataset, training = preprocess_data(firm, 'all')
    _, last_date, _ = forecast_data(firm)
    predictions, forecast = predict(firm, forecast_timeperiod)
    forecast = np.ravel(forecast)

    # Split dataset into training and testing data and add predictions
    train = dataset[:training]
    test = dataset[training:]
    test.insert(1, 'Predictions', predictions)

    # Create dataset of future forecast
    data = {'Date': [last_date], 'Forecast': [forecast[0]]}
    data = pd.DataFrame(data)
    data['Date'] = pd.to_datetime(data['Date'])
    last_date = data['Date'].loc[data.index[0]]
    for i in range(forecast_timeperiod - 1):
        data.loc[len(data.index)] = [(last_date + pd.DateOffset(days=(i+1))), forecast[i+1]]
    data['Date'] = data['Date'] + pd.DateOffset(days=1)

    # Calculate the evaluation metrics for the predictions
    mse = np.mean(((predictions - y_test) ** 2))
    mape = np.round((np.mean((np.abs(y_test - predictions)/y_test)*100)),2)
    return train, test, data, mse, mape
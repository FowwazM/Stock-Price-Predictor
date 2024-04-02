import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import MinMaxScaler
from preprocessing import preprocess_data, forecast_data

def predict(firm, period):
    # Check if firm has been provided by function caller
    if firm == '':
        firm = str(input("Please input the ticker of a firm on the S&P500: "))
    
    # Import preprocessed datasets
    x_train, y_train, x_test, _, scaler = preprocess_data(firm.upper(), '')
    
    # Build the LSTM-gated RNN cells for neural network
    model = keras.models.Sequential()
    model.add(keras.layers.LSTM(units=64,
                                return_sequences=True,
                                input_shape=(x_train.shape[1], 1)))
    model.add(keras.layers.LSTM(units=64))
    model.add(keras.layers.Dense(32))
    model.add(keras.layers.Dropout(0.5))
    model.add(keras.layers.Dense(1))

    # Model compilation and training
    model.compile(optimizer='adam',
                  loss='mean_squared_error')
    history = model.fit(x_train,
                        y_train,
                        epochs=15)
    
    # Test the model by predicting the the testing data
    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)
    
    # Import preprocessed forecasting dataset
    forecast = forecast_data(firm.upper())[0]

    # Generate models future stock price predictions for the next month
    forecast_timeperiod = period

    for i in range(forecast_timeperiod):
        x_input = forecast[:, (len(forecast) - 14):, :]
        prediction = model.predict(x_input)
        forecast = np.concatenate((forecast, prediction[None, :, :]), axis=1)

    forecast = forecast[:, 14:, :]
    forecast = forecast.reshape(-1,1)
    forecast = scaler.inverse_transform(forecast)

    return predictions, forecast
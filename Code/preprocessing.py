import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Load the dataset into a pandas dataframe
data = pd.read_csv('../sp500_stocks.csv')
print(data.shape)
print(data.sample(7))

# Convert 'Date' column from the object date type to DateTime data type
data['Date'] = pd.to_datetime(data['Date'])

# Remove any columns with empty or invalid values
data = data.dropna()

# Filter data on adjusted closing values of stocks of one firm and select training amount
firm = str(input("Please input the ticker of a firm on the S&P500: "))
firm = data[data['Symbol'] == firm]
close_data = firm.filter(['Adj Close'])
close_data = close_data.values
training = int(np.ceil(len(close_data) * 0.8))

# Apply scaling to closing data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(close_data)

# Create subset of the scaled data for training and testing
train_data = scaled_data[0:int(training), :]
test_data = scaled_data[training - 60:, :]

# Prepare features and labels
x_train = []
y_train = []
x_test = []
y_test = []

# Add data values to features and labels (for training)
for i in range(14, len(train_data)):
    x_train.append(train_data[i-14:i, 0])
    y_train.append(train_data[i, 0])

# Add data values to features and labels (for testing)
y_test = close_data[training:, :]
for i in range(60, len(test_data)):
    x_test.append(test_data[i-60:i, 0])

# Transform features and labels into numpy arrays
x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
x_test, y_test = np.array(x_test), np.array(y_test)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
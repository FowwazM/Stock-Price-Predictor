import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import MinMaxScaler
import preprocessing

# Import training set from preprocessed data
x_train = preprocessing.x_train
y_train = preprocessing.y_train

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

# Import test set from preprocessed data
x_test = preprocessing.x_test
y_test = preprocessing.y_test

# Test the model by predicting the the testing data
scaler = preprocessing.scaler
predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)
import matplotlib.pyplot as plt
import numpy as np
import preprocessing
import model

# Import datasets and model predictions
firm_name = preprocessing.firm_name
dataset = preprocessing.firm_data
training = preprocessing.training
y_test = preprocessing.y_test
predictions = model.predictions

# Split dataset into training and testing data and add predictions
train = dataset[:training]
test = dataset[training:]
test.insert(1, 'Predictions', predictions)

# Calculate the evaluation metrics for the predictions
mse = np.mean(((predictions - y_test) ** 2))
print("MSE", mse)
print("RMSE", np.sqrt(mse))

# Plot the training data along with predictions against testing data
plt.figure(figsize=(10, 8))
plt.plot(train['Date'], train['Adj Close'])
plt.plot(test['Date'], test[['Adj Close', 'Predictions']])
plt.title(firm_name + ' Stock Close Price')
plt.xlabel('Date')
plt.ylabel("Close")
plt.legend(['Train', 'Test', 'Predictions'])
plt.show()
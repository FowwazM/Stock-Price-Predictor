import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset into a pandas dataframe
data = pd.read_csv('../sp500_stocks.csv')
print(data.shape)
print(data.sample(7))

# Convert 'Date' column from the object date type to DateTime data type
data['Date'] = pd.to_datetime(data['Date'])

# Choose a list of nine companies to plot
companies = ['AAPL', 'NVDA', 'AMD',
             'GOOGL', 'AMZN', 'META',
             'CVX', 'XOM', 'SLB']

# Plot the opening and (adjusted) closing prices against time
plt.figure(1, figsize=(15, 8))
for index, company in enumerate(companies, 1):
    plt.subplot(3, 3, index)
    c = data[data['Symbol'] == company]
    plt.plot(c['Date'], c['Adj Close'], c="r", label="close", marker="+")
    plt.plot(c['Date'], c['Open'], c="g", label="open", marker="^")
    plt.title(company)
    plt.legend()
    plt.tight_layout()

# Plot the volume against time for the nine companies
plt.figure(2, figsize=(15, 8))
for index, company in enumerate(companies, 1):
    plt.subplot(3, 3, index)
    c = data[data['Symbol'] == company]
    plt.plot(c['Date'], c['Volume'], c='purple', marker='*')
    plt.title(f"{company} Volume")
    plt.tight_layout()

plt.show()
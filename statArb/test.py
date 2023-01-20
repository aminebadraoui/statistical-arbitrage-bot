from datetime import datetime
import requests
import json
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.model_selection import train_test_split

# Coinmarketcap API endpoint
url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'

# Date to convert
date_str = 'October 11, 2020'
date_now = datetime.now()

# Convert the date string to a datetime object
date_obj = datetime.strptime(date_str, '%B %d, %Y')

# Convert the datetime object to a UNIX timestamp
timestamp_from = int(date_obj.timestamp())
timestamp_to = int(date_now.timestamp())

print(timestamp_from)
print(timestamp_to)

# # Your API key
# api_key = '61f03f0a-34a2-4436-89b6-cfd4d99ced0b'

# Parameters for the API request
parameters = {
    'vs_currency': 'usd',
    'days': 'max',
}

# Adding the API key to the headers
headers = {
    'Accepts': 'application/json',
}

# Send the GET request to the API
response = requests.get(url, headers=headers, params=parameters)

# Get the JSON data from the response
data = json.loads(response.text)

print(data)
# Create a DataFrame with the returned data
df = pd.DataFrame(data['data'])

# Select relevant variables
X = df[['volume', 'market_cap']]
y = df['close']

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Linear Regression
model = LinearRegression().fit(X_train, y_train)
pred_price = model.predict(X_test)

# Evaluation
print(f'R-squared: {r2_score(y_test, pred_price)}')
print(f'Root mean squared error: {np.sqrt(mean_squared_error(y_test, pred_price))}')

# Model Interpretation
print(f'Coefficients: {model.coef_}')
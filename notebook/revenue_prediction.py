import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error, mean_absolute_percentage_error, r2_score

"""## Read and Preprocess Data"""

data = pd.read_csv("/content/revenue_data.csv")
data.head()

# Convert the 'date' column to numerical representation (e.g., days since a reference date)
data['date'] = pd.to_datetime(data['date'])
data['days_since_start'] = (data['date'] - data['date'].min()).dt.days

data.head()

data.describe()

# Visualisasi
plt.figure(figsize=(12, 6))
plt.plot(data['date'], data['revenue_juta'])
plt.xlabel('Date')
plt.ylabel('Revenue')
plt.title('Revenue Trend Over Time')
plt.grid(True)
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.locator_params(axis='x', nbins=10) # reduce number of x-ticks, reduce to 10
plt.tight_layout() # Adjust layout to prevent labels from overlapping
plt.show()

"""## Split the Data"""

# Define features (X) and target (y)
X = data[['days_since_start']]
y = data['revenue_juta']

# Split the data into training (80%) and testing sets (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

"""# Modeling

## Training
"""

# Create and train the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Get the coefficients
beta0 = model.intercept_
beta1 = model.coef_[0]

# Print the formula
print(f"revenue = {beta0:.4f} + {beta1:.4f}*date")

"""## Prediction and Visualization"""

# Make predictions using the test set
y_pred = model.predict(X_test)

# Create the plot
plt.figure(figsize=(10, 6))
plt.scatter(data['date'], data['revenue_juta'], label='Actual Revenue')
plt.plot(data['date'][X_test.index], y_pred, color='red', label='Predicted Revenue')
plt.xlabel('Date')
plt.ylabel('Revenue (juta)')
plt.title('Actual vs. Predicted Revenue with Regression Line')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

"""## Evaluation"""

# Evaluate the model
mape = mean_absolute_percentage_error(y_test, y_pred)
rmse = root_mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Percentage Error: {mape*100}%")
print(f"Root Mean Squared Error: {rmse}")
print(f"R-squared: {r2}")

# Example: Predict revenue for a future date
# Convert the future date to days since the start date
future_date = pd.to_datetime('2024-01-15')  # Example future date
future_days = (future_date - data['date'].min()).days
future_revenue = model.predict(np.array([[future_days]]))

print(f"Predicted revenue for {future_date}: {future_revenue[0]} juta")

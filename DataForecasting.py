import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import mysql.connector

class DemandForecaster:
    def __init__(self, host, user, password, database, table):
        self.data = self.fetch_data_from_mysql(host, user, password, database, table)
        self.preprocess_data()
        self.train, self.test = self.split_data()

    def fetch_data_from_mysql(self, host, user, password, database, table):
        try:
            connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(f"SELECT * FROM {table}")
                data = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                df = pd.DataFrame(data, columns=columns)
                cursor.close()
                connection.close()
                return df
        except mysql.connector.Error as e:
            print("Error while connecting to MySQL", e)
            return None

    def preprocess_data(self):
        self.data = self.data.dropna()
        # Add preprocessing steps if needed
        pass

    def split_data(self, test_size=0.2, shuffle=False):
        return train_test_split(self.data, test_size=test_size, shuffle=shuffle)

    def time_series_forecast(self):
        model_ts = ExponentialSmoothing(self.train['demand'], trend='add', seasonal='add', seasonal_periods=12)
        fitted_model_ts = model_ts.fit()
        self.forecast_ts = fitted_model_ts.forecast(len(self.test))

    def gbm_forecast(self):
        X_train = self.train.drop('demand', axis=1)
        y_train = self.train['demand']
        gbm = GradientBoostingRegressor()
        gbm.fit(X_train, y_train)
        self.forecast_gbm = gbm.predict(self.test.drop('demand', axis=1))

    def ensemble_forecast(self):
        self.forecast_ensemble = (self.forecast_ts + self.forecast_gbm) / 2

    def evaluate_performance(self):
        mse = mean_squared_error(self.test['demand'], self.forecast_ensemble)
        mae = mean_absolute_error(self.test['demand'], self.forecast_ensemble)
        r2 = r2_score(self.test['demand'], self.forecast_ensemble)
        return mse, mae, r2

    def run_forecasting(self):
        self.time_series_forecast()
        self.gbm_forecast()
        self.ensemble_forecast()
        return self.evaluate_performance()

    def visualize_forecasts(self):
        # Plot actual vs predicted demand
        plt.figure(figsize=(10, 6))
        plt.plot(self.test.index, self.test['demand'], label='Actual Demand', color='blue')
        plt.plot(self.test.index, self.forecast_ensemble, label='Predicted Demand', color='red')
        plt.title('Actual vs Predicted Demand')
        plt.xlabel('Date')
        plt.ylabel('Demand')
        plt.legend()
        plt.show()

# Usage
host = 'your_host'
user = 'your_username'
password = 'password'
database = 'SupplyChainDB'
table = 'DemandForecasting_data'

forecaster = DemandForecaster(host, user, password, database, table)
mse, mae, r2 = forecaster.run_forecasting()
print(f'Mean Squared Error: {mse}')
print(f'Mean Absolute Error: {mae}')
print(f'R-squared: {r2}')

# Visualize forecasts
forecaster.visualize_forecasts()

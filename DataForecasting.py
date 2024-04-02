import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import mysql.connector
import matplotlib.pyplot as plt

class DemandForecaster:
    def __init__(self, data):
        self.data = data
        self.preprocess_data()
        self.train, self.test = self.split_data()

    def preprocess_data(self):
        self.data = self.data.dropna()
        #self.data['Date'] = pd.to_datetime(self.data['Date'])

    def split_data(self, test_size=0.2, shuffle=False):
        return train_test_split(self.data, test_size=test_size, shuffle=shuffle)

    def time_series_forecast(self):
        print(self.train.columns)
        model_ts = ExponentialSmoothing(self.train['SalesVolume'], trend='add', seasonal='add', seasonal_periods=12)
        fitted_model_ts = model_ts.fit()
        self.forecast_ts = fitted_model_ts.forecast(len(self.test))

    def gbm_forecast(self):
        X_train = self.train.drop('SalesVolume', axis=1)
        y_train = self.train['SalesVolume']
        gbm = GradientBoostingRegressor()
        gbm.fit(X_train, y_train)
        self.forecast_gbm = gbm.predict(self.test.drop('SalesVolume', axis=1))

    def ensemble_forecast(self):
        self.forecast_ensemble = (self.forecast_ts + self.forecast_gbm) / 2

    def evaluate_performance(self):
        mse = mean_squared_error(self.test['SalesVolume'], self.forecast_ensemble)
        mae = mean_absolute_error(self.test['SalesVolume'], self.forecast_ensemble)
        r2 = r2_score(self.test['SalesVolume'], self.forecast_ensemble)
        return mse, mae, r2

    def run_forecasting(self):
        self.time_series_forecast()
        self.gbm_forecast()
        self.ensemble_forecast()
        return self.evaluate_performance()

class DataProcessor:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def fetch_data_from_mysql(self, table_name, batch_size=1000):
        connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

        processed_data = []
        try:
            if connection.is_connected():
                cursor = connection.cursor()

                for offset in range(0, 500000, batch_size):
                    sql = f"SELECT * FROM {table_name} LIMIT {batch_size} OFFSET {offset}"
                    cursor.execute(sql)
                    data = cursor.fetchall()
                    df = pd.DataFrame(data)
                    processed_data.append(df)

                cursor.close()
                print("Data fetching completed.")

        except mysql.connector.Error as e:
            print("Error while fetching data from MySQL", e)

        finally:
            if connection.is_connected():
                connection.close()

        return pd.concat(processed_data)

    def plot_data(self, df):
        plt.figure(figsize=(10, 6))
        plt.plot(df['Date'], df['SalesVolume'], marker='o', linestyle='-')
        plt.title('Sales Volume Over Time')
        plt.xlabel('Date')
        plt.ylabel('Sales Volume')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    processor = DataProcessor('localhost', 'root', 'password', 'SupplyChainDB')
    data_df = processor.fetch_data_from_mysql('DemandForecasting')
    forecaster = DemandForecaster(data_df)
    mse, mae, r2 = forecaster.run_forecasting()
    print(f'Mean Squared Error: {mse}')
    print(f'Mean Absolute Error: {mae}')
    print(f'R-squared: {r2}')
    processor.plot_data(data_df)
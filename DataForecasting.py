import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

class DemandForecaster:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)
        self.preprocess_data()
        self.train, self.test = self.split_data()

    def preprocess_data(self):
        self.data = self.data.dropna()
        self.data['date'] = pd.to_datetime(self.data['date'])
        self.data.set_index('date', inplace=True)

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

# Usage
forecaster = DemandForecaster('demand_data.csv')
mse, mae, r2 = forecaster.run_forecasting()
print(f'Mean Squared Error: {mse}')
print(f'Mean Absolute Error: {mae}')
print(f'R-squared: {r2}')
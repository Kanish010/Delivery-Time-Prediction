import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt

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

    def extract_features(self, data):
        data['day_of_week'] = data.index.dayofweek
        data['month'] = data.index.month
        data['quarter'] = data.index.quarter
        return data

    def time_series_forecast(self):
        model_ts = ExponentialSmoothing(self.train['demand'], trend='add', seasonal='add', seasonal_periods=12)
        fitted_model_ts = model_ts.fit()
        self.forecast_ts = fitted_model_ts.forecast(len(self.test))

    def gbm_forecast(self):
        X_train = self.train.drop('demand', axis=1)
        y_train = self.train['demand']
        gbm = GradientBoostingRegressor()
        param_grid = {'n_estimators': [50, 100, 200], 'max_depth': [3, 5, 7]}
        gbm_grid = GridSearchCV(gbm, param_grid, cv=3, n_jobs=-1)
        gbm_grid.fit(X_train, y_train)
        self.gbm_best = gbm_grid.best_estimator_
        self.forecast_gbm = self.gbm_best.predict(self.test.drop('demand', axis=1))

    def ensemble_forecast(self):
        self.forecast_ensemble = (self.forecast_ts + self.forecast_gbm) / 2

    def evaluate_performance(self):
        mse = mean_squared_error(self.test['demand'], self.forecast_ensemble)
        mae = mean_absolute_error(self.test['demand'], self.forecast_ensemble)
        r2 = r2_score(self.test['demand'], self.forecast_ensemble)
        return mse, mae, r2

    def visualize_forecast(self):
        plt.plot(self.test.index, self.test['demand'], label='Actual Demand')
        plt.plot(self.test.index, self.forecast_ensemble, label='Forecasted Demand (Ensemble)')
        plt.xlabel('Date')
        plt.ylabel('Demand')
        plt.title('Demand Forecasting')
        plt.legend()
        plt.show()

    def run_forecasting(self):
        self.train = self.extract_features(self.train)
        self.test = self.extract_features(self.test)
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
forecaster.visualize_forecast()
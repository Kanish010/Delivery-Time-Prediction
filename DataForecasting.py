import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import xgboost as xgb
import tensorflow as tf
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import mysql.connector
import matplotlib.pyplot as plt

class DemandForecaster:
    def __init__(self, host, user, password, database, table_name, batch_size=1000):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.table_name = table_name
        self.batch_size = batch_size

    def fetch_data_from_mysql(self):
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

                for offset in range(0, 500000, self.batch_size):
                    sql = f"SELECT * FROM {self.table_name} LIMIT {self.batch_size} OFFSET {offset}"
                    cursor.execute(sql)
                    data = cursor.fetchall()
                    df = pd.DataFrame(data, columns=['ProductID', 'Date', 'SalesVolume', 'Price', 'Promotion', 
                                                     'Category', 'Brand', 'SeasonalityFactor', 'CompetitorPresence', 
                                                     'WeatherCondition'])
                    processed_data.append(df)

                cursor.close()
                print("Data fetching completed.")

        except mysql.connector.Error as e:
            print("Error while fetching data from MySQL", e)

        finally:
            if connection.is_connected():
                connection.close()

        self.data = pd.concat(processed_data, ignore_index=True)

    def preprocess_data(self):
        self.data = self.data.dropna()
        self.data.drop(columns=['Date'], inplace=True)
        self.data.reset_index(drop=True, inplace=True)

    def split_data(self, test_size=0.2, shuffle=False):
        X = self.data.drop('SalesVolume', axis=1)
        y = self.data['SalesVolume']
        return train_test_split(X, y, test_size=test_size, shuffle=shuffle)

    def build_lstm_model(self, input_shape):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(500, activation="relu"),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(400, activation="relu"),
            tf.keras.layers.Dropout(0.4),
            tf.keras.layers.Dense(300, activation="relu"),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(200, activation="relu"),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(100, activation="relu"),
            tf.keras.layers.Dropout(0.1),
            tf.keras.layers.Dense(1)
        ])
        model.compile(optimizer='adam', loss='mse')
        return model

    def build_xgboost_model(self):
        model = xgb.XGBRegressor(objective ='reg:squarederror')
        return model

    def train_lstm_model(self, X_train, y_train, epochs=100, batch_size=32):
        model = self.build_lstm_model(input_shape=(X_train.shape[1], X_train.shape[2]))
        model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=1)
        return model

    def train_xgboost_model(self, X_train, y_train):
        model = self.build_xgboost_model()
        model.fit(X_train, y_train)
        return model

    def evaluate_performance(self, y_true, y_pred):
        mse = mean_squared_error(y_true, y_pred)
        mae = mean_absolute_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)
        return mse, mae, r2

    def plot_actual_vs_predicted(self, y_true, y_pred):
        plt.figure(figsize=(10, 6))
        plt.plot(y_true, label='Actual', marker='o', linestyle='-')
        plt.plot(y_pred, label='Predicted', marker='o', linestyle='--')
        plt.title('Actual vs Predicted Sales Volume')
        plt.xlabel('Index')
        plt.ylabel('Sales Volume')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def run_forecasting(self):
        self.fetch_data_from_mysql()
        self.preprocess_data()

        X_train, X_test, y_train, y_test = self.split_data()
        
        # Normalize data
        scaler = MinMaxScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        y_train_scaled = scaler.fit_transform(y_train.reshape(-1, 1))
        
        # Reshape data for LSTM
        X_train_reshaped = X_train_scaled.reshape((X_train_scaled.shape[0], 1, X_train_scaled.shape[1]))
        X_test_reshaped = X_test_scaled.reshape((X_test_scaled.shape[0], 1, X_test_scaled.shape[1]))
        
        # Train LSTM model
        lstm_model = self.train_lstm_model(X_train_reshaped, y_train_scaled)
        
        # Train XGBoost model
        xgb_model = self.train_xgboost_model(X_train, y_train)
        
        # Make predictions using LSTM
        y_pred_scaled_lstm = lstm_model.predict(X_test_reshaped)
        y_pred_lstm = scaler.inverse_transform(y_pred_scaled_lstm).flatten()
        
        # Make predictions using XGBoost
        y_pred_xgb = xgb_model.predict(X_test)
        
        # Ensemble predictions (simple averaging)
        y_pred_ensemble = (y_pred_lstm + y_pred_xgb) / 2
        
        # Plot actual vs predicted
        self.plot_actual_vs_predicted(y_test, y_pred_ensemble)
        
        # Evaluate performance
        mse, mae, r2 = self.evaluate_performance(y_test, y_pred_ensemble)
        return mse, mae, r2

if __name__ == "__main__":
    forecaster = DemandForecaster('localhost', 'root', 'password', 'SupplyChainDB', 'DemandForecasting')
    mse, mae, r2 = forecaster.run_forecasting()
    print(f'Mean Squared Error: {mse}')
    print(f'Mean Absolute Error: {mae}')
    print(f'R-squared: {r2}')
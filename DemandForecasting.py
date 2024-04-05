import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import mysql.connector
import matplotlib.pyplot as plt
import tensorflow as tf
from keras.callbacks import EarlyStopping

class DemandForecaster:
    def __init__(self, host, user, password, database, table_name, batch_size=32):
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

                for offset in range(0, 5000, self.batch_size):  
                    sql = f"SELECT SalesVolume, Price, Promotion, Category, Brand, SeasonalityFactor, CompetitorPresence, WeatherCondition FROM {self.table_name} LIMIT {self.batch_size} OFFSET {offset}"
                    cursor.execute(sql)
                    data = cursor.fetchall()
                    df = pd.DataFrame(data, columns=['SalesVolume', 'Price', 'Promotion', 
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

        # Convert categorical variables to numeric using LabelEncoder
        label_encoders = {}
        for column in ['Promotion', 'Category', 'Brand', 'WeatherCondition']:
            label_encoders[column] = LabelEncoder()
            self.data[column] = label_encoders[column].fit_transform(self.data[column])

        # Map 'SeasonalityFactor' to numerical values
        season_mapping = {'Spring': 0, 'Summer': 1, 'Fall': 2, 'Winter': 3}
        self.data['SeasonalityFactor'] = self.data['SeasonalityFactor'].map(season_mapping)

        # Normalize numerical features
        scaler = MinMaxScaler()
        self.data[['SalesVolume', 'Price', 'CompetitorPresence']] = scaler.fit_transform(self.data[['SalesVolume', 'Price', 'CompetitorPresence']])

        self.data.reset_index(drop=True, inplace=True)

    def split_data(self, test_size=0.2, shuffle=False):
        X = self.data.drop('SalesVolume', axis=1)
        y = self.data['SalesVolume']
        return train_test_split(X, y, test_size=test_size, shuffle=shuffle)

    def build_lstm_model(self, input_shape):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(256, activation="relu"),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(64, activation="relu"),
            tf.keras.layers.Dropout(0.1),
            tf.keras.layers.Dense(1)
        ])
        model.compile(optimizer='adam', loss='mse')
        return model

    def train_lstm_model(self, X_train, y_train, epochs=5, batch_size=32):
        input_shape = (X_train.shape[1],)
        model = self.build_lstm_model(input_shape)
        
        # Early stopping callback
        early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
        
        # Training the model
        history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=1, validation_split=0.2, callbacks=[early_stopping])
        return model, history

    def build_random_forest_model(self):
        return RandomForestRegressor(n_estimators=100, random_state=42)

    def train_model(self, model, X_train, y_train):
        model.fit(X_train, y_train)
        return model

    def evaluate_performance(self, y_true, y_pred):
        mse = mean_squared_error(y_true, y_pred)
        mae = mean_absolute_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)
        return mse, mae, r2

    def plot_actual_vs_predicted(self, y_true, y_pred):
        plt.figure(figsize=(10, 6))
        plt.scatter(y_true, y_pred, alpha=0.5)
        plt.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], 'k--', lw=2)
        plt.title('Actual vs Predicted Sales Volume')
        plt.xlabel('Actual Sales Volume')
        plt.ylabel('Predicted Sales Volume')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def run_forecasting(self):
        self.fetch_data_from_mysql()
        self.preprocess_data()

        X_train, X_test, y_train, y_test = self.split_data()
        
        # Train LSTM model
        lstm_model, _ = self.train_lstm_model(X_train, y_train)
        
        # Train Random Forest model
        rf_model = self.build_random_forest_model()
        rf_model.fit(X_train, y_train)
        
        # Make predictions using LSTM
        y_pred_lstm = lstm_model.predict(X_test).flatten()
        
        # Make predictions using Random Forest
        y_pred_rf = rf_model.predict(X_test)

        # Combine predictions (ensemble)
        y_pred_ensemble = (y_pred_lstm + y_pred_rf) / 2
        
        # Plot actual vs ensemble predicted
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
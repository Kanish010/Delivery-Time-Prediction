import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import mysql.connector
import matplotlib.pyplot as plt

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
        
        # Build and train Random Forest model
        rf_model = self.build_random_forest_model()
        trained_model = self.train_model(rf_model, X_train, y_train)
        
        # Make predictions using Random Forest
        y_pred_rf = trained_model.predict(X_test)

        # Plot actual vs predicted
        self.plot_actual_vs_predicted(y_test, y_pred_rf)
        
        # Evaluate performance
        mse, mae, r2 = self.evaluate_performance(y_test, y_pred_rf)
        return mse, mae, r2

if __name__ == "__main__":
    forecaster = DemandForecaster('localhost', 'root', 'password', 'SupplyChainDB', 'DemandForecasting')
    mse, mae, r2 = forecaster.run_forecasting()
    print(f'Mean Squared Error: {mse}')
    print(f'Mean Absolute Error: {mae}')
    print(f'R-squared: {r2}')
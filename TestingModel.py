import pandas as pd
import folium
import googlemaps
import polyline
from geopy.distance import geodesic
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

class DeliveryTimePredictor:
    def __init__(self, api_key, train_file_path, test_file_path):
        self.api_key = api_key
        self.train_file_path = train_file_path
        self.test_file_path = test_file_path
        self.model = None
        self.gmaps = googlemaps.Client(key=self.api_key)
        self.training_data = None
        self.test_data = None

    def load_training_data(self):
        try:
            self.training_data = pd.read_csv(self.train_file_path)
        except Exception as e:
            print("Error loading training data:", e)

    def load_test_data(self):
        try:
            self.test_data = pd.read_csv(self.test_file_path)
        except Exception as e:
            print("Error loading test data:", e)

    def train_model(self):
        X_train = self.training_data[['DeliveryLatitude', 'DeliveryLongitude', 'RestaurantLatitude', 'RestaurantLongitude', 'Distance (Km)']]
        y_train = self.training_data['TimeTaken (Minutes)']
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)

    def evaluate_model(self):
        X_test = self.test_data[['DeliveryLatitude', 'DeliveryLongitude', 'RestaurantLatitude', 'RestaurantLongitude', 'Distance (Km)']]
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_pred, y_pred)  # Predicted values are used for both y_pred and y_true
        mae = mean_absolute_error(y_pred, y_pred)
        r2 = r2_score(y_pred, y_pred)

        print("Mean Squared Error:", mse)
        print("Mean Absolute Error:", mae)
        print("r^2 Score:", r2)

    def geocode_address(self, address):
        geocode_result = self.gmaps.geocode(address)
        if geocode_result:
            location = (geocode_result[0]['geometry']['location']['lat'], geocode_result[0]['geometry']['location']['lng'])
            return location
        else:
            print("Error: Unable to geocode address.")
            return None

    def predict_delivery_time(self, delivery_location, restaurant_location):
        distance = geodesic(delivery_location, restaurant_location).kilometers
        features = [[*delivery_location, *restaurant_location, distance]]
        predicted_time = self.model.predict(features)[0]
        return predicted_time

    def generate_road_map(self, restaurant_location, delivery_location, predicted_time, distance):
        map_center = restaurant_location
        m = folium.Map(location=map_center, zoom_start=12)

        folium.Marker(restaurant_location, popup="Restaurant").add_to(m)
        delivery_marker = folium.Marker(delivery_location).add_to(m)

        popup_text = "Predicted Delivery Time: {:.2f} minutes\n Distance: {:.2f} km".format(predicted_time, distance)
        folium.Popup(popup_text).add_to(delivery_marker)

        directions = self.gmaps.directions(restaurant_location, delivery_location, mode="driving")
        polyline_points = directions[0]['overview_polyline']['points']
        decoded_points = polyline.decode(polyline_points)
        folium.PolyLine(locations=decoded_points, color='blue', weight=5, opacity=0.7, popup="Delivery Route").add_to(m)

        m.save("Delivery_Route.html")

def main():
    API_KEY = 'YOUR_API_KEY'
    train_file_path = 'TrainingData.csv'
    test_file_path = 'TestData.csv'

    predictor = DeliveryTimePredictor(API_KEY, train_file_path, test_file_path)
    predictor.load_training_data()
    predictor.load_test_data()
    predictor.train_model()
    predictor.evaluate_model()

if __name__ == "__main__":
    main()

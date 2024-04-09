import pandas as pd
import folium
import googlemaps
import polyline
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from geopy.distance import geodesic

class DeliveryTimePredictor:
    def __init__(self, api_key, file_path):
        self.api_key = api_key
        self.file_path = file_path
        self.model = None
        self.gmaps = googlemaps.Client(key=self.api_key)
        self.training_data = None

    def load_training_data(self):
        try:
            self.training_data = pd.read_csv(self.file_path)
        except Exception as e:
            print("Error loading training data:", e)

    def train_model(self):
        X = self.training_data[['DeliveryLatitude', 'DeliveryLongitude', 'RestaurantLatitude', 'RestaurantLongitude', 'Distance (Km)']]
        y = self.training_data['TimeTaken (Minutes)']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        print("Mean Squared Error:", mse)
        print("Mean Absolute Error:", mae)
        print("r^2 Score:", r2)

    def predict_delivery_time(self, delivery_location, restaurant_location):
        distance = geodesic(delivery_location, restaurant_location).kilometers
        features = np.array([delivery_location[0], delivery_location[1], 
                             restaurant_location[0], restaurant_location[1], distance]).reshape(1, -1)
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
    file_path = 'TrainingData.csv'
    delivery_location = (1.3196, 103.7525)
    restaurant_location = (1.2964, 103.7925)

    predictor = DeliveryTimePredictor(API_KEY, file_path)
    predictor.load_training_data()
    predictor.train_model()

    distance = geodesic(delivery_location, restaurant_location).kilometers
    predicted_time = predictor.predict_delivery_time(delivery_location, restaurant_location)
    predictor.generate_road_map(restaurant_location, delivery_location, predicted_time, distance)

if __name__ == "__main__":
    main()

import pandas as pd
import folium
import googlemaps
import polyline
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Google Maps API Key
API_KEY = 'YOUR_API_KEY'

def load_training_data(file_path):
    try:
        data = pd.read_csv("TrainingData.csv")
        return data
    except Exception as e:
        print("Error loading training data:", e)
        return None

def generate_road_map(restaurant_location, delivery_location, predicted_time, gmaps):
    # Create a folium map centered at the restaurant location
    map_center = restaurant_location
    m = folium.Map(location=map_center, zoom_start=12)

    # Add marker for restaurant and delivery location
    folium.Marker(restaurant_location, popup="Restaurant").add_to(m)
    delivery_marker = folium.Marker(delivery_location).add_to(m)

    # Concatenate popup text
    popup_text = "Predicted Delivery Time: {} minutes".format(predicted_time)

    # Add delivery duration as popup
    folium.Popup(popup_text).add_to(delivery_marker)

    # Generate road map with route polyline
    directions = gmaps.directions(restaurant_location, delivery_location, mode="driving")
    polyline_points = directions[0]['overview_polyline']['points']
    decoded_points = polyline.decode(polyline_points)
    folium.PolyLine(locations=decoded_points, color='blue', weight=5, opacity=0.7, popup="Delivery Route").add_to(m)

    # Save the map to an HTML file or display it
    m.save("Delivery_Route.html")

def train_model(data):
    X = data[['DeliveryLatitude', 'DeliveryLongitude', 'RestaurantLatitude', 'RestaurantLongitude']]
    y = data['TimeTaken (Minutes)']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
    return model

def main():
    # Load training data from CSV
    training_data = load_training_data('TrainingData.csv')
    if training_data is None:
        return

    # Sample delivery location and restaurant location (to be input by the user)
    delivery_location = (1.3196, 103.7525)  # Example coordinates
    restaurant_location = (1.2964, 103.7925)  # Example coordinates

    # Initialize Google Maps client
    gmaps = googlemaps.Client(key=API_KEY)

    # Train model
    model = train_model(training_data)

    # Predict delivery time
    predicted_time = model.predict(np.array([delivery_location[0], delivery_location[1], 
                                             restaurant_location[0], restaurant_location[1]]).reshape(1, -1))[0]

    # Generate road map
    generate_road_map(restaurant_location, delivery_location, predicted_time, gmaps)

if __name__ == "__main__":
    main()
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import StandardScaler
import folium
from folium import plugins
import requests

def preprocess_data(df):
    # Extract features and target variable
    X = df[['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']]
    y = df['Time_taken(min)']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled, y_train, y_test, X

def train_model(X_train, y_train):
    # Train the Random Forest model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    # Make predictions on the test set
    y_pred = model.predict(X_test)

    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    print("Mean Squared Error:", mse)
    print("Mean Absolute Error:", mae)
    return y_pred

def get_route(restaurant_location, delivery_location):
    # Make a request to OSRM API to get the route between two locations
    url = f"http://router.project-osrm.org/route/v1/driving/{restaurant_location[1]},{restaurant_location[0]};{delivery_location[1]},{delivery_location[0]}"
    response = requests.get(url)
    data = response.json()

    # Extract the route geometry
    route_geometry = data['routes'][0]['geometry']['coordinates']
    return route_geometry

def generate_heat_map(restaurant_location, delivery_location, X, model):
    # Create a folium map centered at the restaurant location
    map_center = restaurant_location
    m = folium.Map(location=map_center, zoom_start=12)

    # Add marker for restaurant and delivery location
    folium.Marker(restaurant_location, popup="Restaurant").add_to(m)
    folium.Marker(delivery_location, popup="Delivery Location").add_to(m)

    # Get route between restaurant and delivery location
    route_geometry = get_route(restaurant_location, delivery_location)

    # Draw route on the map
    folium.PolyLine(locations=route_geometry, color="blue", weight=2.5, opacity=1).add_to(m)

    # Predict delivery time using the trained model
    delivery_data = [[restaurant_location[0], restaurant_location[1], delivery_location[0], delivery_location[1]]]
    estimated_duration = model.predict(delivery_data)[0]
    
    # Add popup with estimated duration
    popup_text = f"Estimated Delivery Time: {estimated_duration:.2f} minutes"
    folium.Popup(popup_text).add_to(folium.Marker(delivery_location, popup=popup_text))

    # Save the map to an HTML file or display it
    m.save("heat_map.html")

def main():
    # Load the dataset from CSV file into a DataFrame
    df = pd.read_excel("/Users/kanishalluri/Desktop/Python/Github Projects/Supply-Chain-Optimization/Food Delivery Time Prediction Case Study.xlsx")

    # Preprocess the data
    X_train, X_test, y_train, y_test, X = preprocess_data(df)

    # Train the model
    model = train_model(X_train, y_train)

    # Evaluate the model
    y_pred = evaluate_model(model, X_test, y_test)

    # Sample delivery location and restaurant location (to be input by the user)
    delivery_location = (22.765049, 75.912471)  # Example coordinates
    restaurant_location = (22.745049, 75.892471)  # Example coordinates

    # Generate heat map
    generate_heat_map(restaurant_location, delivery_location, X, model)

if __name__ == "__main__":
    main()
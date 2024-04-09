# Delivery Time Prediction

The Delivery Time Prediction project aims to predict the time it takes for a delivery to reach its destination from a restaurant location in Singapore. This prediction is based on factors such as the geographical coordinates of the delivery and restaurant locations, as well as the distance between them.

This project utilizes machine learning techniques, specifically the RandomForestRegressor algorithm, to train a model on historical delivery data. The trained model can then be used to predict delivery times for new orders based on their locations.

# Dependencies 
Before running the script, make sure to install the required libraries by executing the following command in your terminal or command prompt:

pip install numpy pandas geopandas geopy uuid folium googlemaps polyline sklearn

# Classes
### Delivery Time Optimization
This class encapsulates the functionality related to predicting delivery times and generating road map. It includes methods for loading training data, training the model, predicting delivery times, and generating road maps.

- Key methods include:
  - `load_training_data`: Loads training data from a CSV file.
  - `train_model`: Trains the RandomForestRegressor model on the loaded training data.
  - `predict_delivery_time`: Predicts the delivery time given delivery and restaurant locations.
  - `generate_road_map`: Generates a road map visualization showing the delivery route and predicted delivery time.

### Data Creation
The Data Creation class is responsible for generating synthetic delivery data for training the prediction model. It includes methods for loading boundary data, generating random delivery points within the boundary, and saving the generated data to a CSV file.

- Key methods include:
  - `load_boundary_data`: Loads boundary data from a GeoJSON file.
  - `haversine_distance`: Calculates the great circle distance between two points on the earth's surface.
  - `generate_random_points_within_bounds`: Generates random delivery points within the specified boundary.
  - `save_points_to_csv`: Saves the generated delivery points to a CSV file.

## Model Performance
Mean Squared Error: 0.0014543213246330222
Mean Absolute Error: 0.009358326249831997
r^2 Score: 0.9999913645668616
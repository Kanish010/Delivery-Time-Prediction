import geopandas as gpd
import random
import uuid
from shapely.geometry import Point
import numpy as np
import requests
import time

# Google Maps API Key
API_KEY = 'YOUR_API_KEY'

def load_boundary_data(file_path):
    try:
        boundary_data = gpd.read_file("Singapore.geojson")
        return boundary_data
    except Exception as e:
        print("Error loading boundary data:", e)
        return None

def calculate_distance(origin, destination, api_key):
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin[0]},{origin[1]}&destinations={destination[0]},{destination[1]}&key={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        distance = data['rows'][0]['elements'][0]['distance']['value']
        return distance
    except requests.RequestException as e:
        print("Error during API call:", e)
    except (KeyError, IndexError):
        print("Error: Unable to calculate distance.")
    return None

def generate_random_points_within_bounds(boundary_data, num_points, transport_probabilities, api_key):
    if boundary_data is None:
        return None

    minx, miny, maxx, maxy = boundary_data.total_bounds
    
    # Generate random latitude and longitude for the restaurant within Singapore bounds
    restaurant_latitude = random.uniform(miny, maxy)
    restaurant_longitude = random.uniform(minx, maxx)
    
    # Start with a grid size equal to the square root of the desired number of points
    grid_size = int(np.sqrt(num_points))
    random_points = []
    
    while len(random_points) < num_points:
        grid_x = np.linspace(minx, maxx, grid_size)
        grid_y = np.linspace(miny, maxy, grid_size)

        for x in grid_x:
            for y in grid_y:
                random_lat = random.uniform(y, y + (maxy - miny) / grid_size)
                random_lon = random.uniform(x, x + (maxx - minx) / grid_size)
                
                # Randomly select a transport type based on probabilities
                transport_type = random.choices(list(transport_probabilities.keys()), weights=transport_probabilities.values())[0]
                
                # Generate a unique delivery ID
                delivery_id = str(uuid.uuid4().hex)[:10]  
                
                # Create a point object
                point = Point(random_lon, random_lat)

                # Check if the point falls within the boundary
                if boundary_data.contains(point).any():
                    # Calculate distance between restaurant and delivery point
                    distance = calculate_distance((restaurant_latitude, restaurant_longitude), (random_lat, random_lon), api_key)
                    if distance is not None:
                        # Assuming a speed of 30 km/h, calculate time in minutes
                        time_taken = distance / (60 * 1000 / 60)  # Convert speed to meters per minute
                        random_points.append({'Delivery_ID': delivery_id, 
                                              'DeliveryLongitude': random_lon, 
                                              'DeliveryLatitude': random_lat, 
                                              'RestaurantLatitude': restaurant_latitude, 
                                              'RestaurantLongitude': restaurant_longitude,
                                              'Transport': transport_type,
                                              'TimeTaken (Minutes)': time_taken})
                        if len(random_points) >= num_points:
                            return random_points
                    else:
                        print("API limit reached. Waiting before making next request...")
                        time.sleep(1)  # Wait for 1 second before making the next request

        # If not enough points were generated, increase the grid size
        grid_size += 1

    return random_points

def save_points_to_csv(points_df, file_path):
    if points_df is None:
        return
    
    try:
        points_df.to_csv(file_path, index=False)
        print("Points saved to CSV successfully.")
    except Exception as e:
        print("Error saving points to CSV:", e)

# Main code execution
if __name__ == "__main__":
    # File path to the boundary data
    boundary_file_path = "Singapore.geojson"

    # Load boundary data
    boundary_data = load_boundary_data(boundary_file_path)

    num_points = 10

    # Generate random points within the bounds of the boundary data
    transport_probabilities = {'motorcycle': 0.5, 'car': 0.2, 'bike': 0.3}  
    random_points = generate_random_points_within_bounds(boundary_data, num_points, transport_probabilities, API_KEY)

    # Convert list of dictionaries to GeoDataFrame
    random_points_gdf = gpd.GeoDataFrame(random_points, geometry=gpd.points_from_xy([point['DeliveryLongitude'] for point in random_points], 
                                                                                    [point['DeliveryLatitude'] for point in random_points]),
                                         crs='EPSG:4326')

    # Save points to CSV
    if not random_points_gdf.empty:
        save_points_to_csv(random_points_gdf[['Delivery_ID', 'Transport', 'DeliveryLatitude', 'DeliveryLongitude', 
                                              'RestaurantLatitude', 'RestaurantLongitude', 'TimeTaken (Minutes)']], "TrainingData.csv")

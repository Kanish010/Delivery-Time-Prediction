import geopandas as gpd
import random

def load_boundary_data(file_path):
    try:
        boundary_data = gpd.read_file(file_path)
        return boundary_data
    except Exception as e:
        print("Error loading boundary data:", e)
        return None

def generate_random_points_within_bounds(boundary_data, num_points, transport_probabilities):
    if boundary_data is None:
        return None

    minx, miny, maxx, maxy = boundary_data.total_bounds
    random_points = []

    for _ in range(num_points):
        random_lat = random.uniform(miny, maxy)
        random_lon = random.uniform(minx, maxx)

        # Randomly select a transport type based on probabilities
        transport_type = random.choices(list(transport_probabilities.keys()), weights=transport_probabilities.values())[0]
        random_points.append({'Longitude': random_lon, 'Latitude': random_lat, 'Transport': transport_type})

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
    boundary_file_path = "File_path"

    # Load boundary data
    boundary_data = load_boundary_data(boundary_file_path)

    # Generate random points within the bounds of the boundary data
    num_points = 100
    transport_probabilities = {'motorcycle': 0.2, 'car': 0.6, 'bike': 0.2}  # Adjust probabilities as needed
    random_points = generate_random_points_within_bounds(boundary_data, num_points, transport_probabilities)

    # Convert list of dictionaries to GeoDataFrame
    random_points_gdf = gpd.GeoDataFrame(random_points, geometry=gpd.points_from_xy([point['Longitude'] for point in random_points], 
                                                                                    [point['Latitude'] for point in random_points]),
                                         crs='EPSG:4326')

    # Filter points within the boundary
    points_within_bounds = gpd.sjoin(random_points_gdf, boundary_data, predicate='within')

    # Save points to CSV
    if not points_within_bounds.empty:
        save_points_to_csv(points_within_bounds[['Longitude', 'Latitude', 'Transport']], "points_within_singapore.csv")
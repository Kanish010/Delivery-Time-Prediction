# Delivery Time Optimization
import geopandas as gpd
import random

def load_boundary_data(file_path):
    try:
        boundary_data = gpd.read_file("/Users/kanishalluri/Desktop/Python/Github Projects/Supply-Chain-Optimization/Singapore.geojson")
        return boundary_data
    except Exception as e:
        print("Error loading boundary data:", e)
        return None

def generate_random_points_within_bounds(boundary_data, num_points):
    if boundary_data is None:
        return None

    minx, miny, maxx, maxy = boundary_data.total_bounds
    random_points = []

    for _ in range(num_points):
        random_lat = random.uniform(miny, maxy)
        random_lon = random.uniform(minx, maxx)
        random_points.append((random_lon, random_lat))

    return random_points

def filter_points_within_bounds(random_points, boundary_data):
    if boundary_data is None or random_points is None:
        return None

    crs = 'EPSG:4326'   # Coordinate Reference System (CRS) for WGS84
    random_points_gdf = gpd.GeoDataFrame(geometry=gpd.points_from_xy(*zip(*random_points)), crs=crs)
    points_within_bounds = gpd.sjoin(random_points_gdf, boundary_data, predicate='within')
    return points_within_bounds

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
    boundary_file_path = "/Users/kanishalluri/Desktop/Python/Github Projects/Supply-Chain-Optimization/Singapore.geojson"

    # Load boundary data
    boundary_data = load_boundary_data(boundary_file_path)

    # Generate random points within the bounds of the boundary data
    num_points = 50
    random_points = generate_random_points_within_bounds(boundary_data, num_points)

    # Filter points within the boundary
    points_within_bounds = filter_points_within_bounds(random_points, boundary_data)

    # Save points to CSV
    if points_within_bounds is not None:
        save_points_to_csv(points_within_bounds, "points_within_singapore.csv")
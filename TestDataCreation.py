import geopandas as gpd
import random
import uuid
from shapely.geometry import Point
from geopy.distance import geodesic
from shapely.ops import unary_union
from concurrent.futures import ProcessPoolExecutor

class DataCreation:
    def __init__(self, boundary_file_path):
        self.boundary_file_path = boundary_file_path
        self.boundary_data = self.load_boundary_data()
        self.restaurant_latitude = None
        self.restaurant_longitude = None

    def load_boundary_data(self):
        try:
            return gpd.read_file(self.boundary_file_path)
        except Exception as e:
            print("Error loading boundary data:", e)
            return None

    def calculate_distance(self, point1, point2):
        """
        Calculate the great circle distance between two points 
        """
        return geodesic(point1, point2).kilometers

    def generate_random_points_within_bounds(self, num_points, transport_probabilities):
        if self.boundary_data is None:
            return None

        minx, miny, maxx, maxy = self.boundary_data.total_bounds
        
        # Create a single polygon for boundary check
        boundary_polygon = unary_union(self.boundary_data.geometry)
        
        random_points = []
        while len(random_points) < num_points:
            # Generate random latitude and longitude within the boundary
            random_point = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
            
            if boundary_polygon.contains(random_point):
                # Randomly select a transport type based on probabilities
                transport_type = random.choices(list(transport_probabilities.keys()), weights=transport_probabilities.values())[0]
                
                # Generate a unique delivery ID
                delivery_id = str(uuid.uuid4().hex)[:10]  
                
                # Calculate distance between restaurant and delivery point
                if self.restaurant_latitude is None or self.restaurant_longitude is None:
                    self.restaurant_latitude = random.uniform(miny, maxy)
                    self.restaurant_longitude = random.uniform(minx, maxx)
                distance = self.calculate_distance((self.restaurant_latitude, self.restaurant_longitude), (random_point.y, random_point.x))
                
                random_points.append({'Delivery_ID': delivery_id, 
                                      'DeliveryLongitude': random_point.x, 
                                      'DeliveryLatitude': random_point.y, 
                                      'RestaurantLatitude': self.restaurant_latitude, 
                                      'RestaurantLongitude': self.restaurant_longitude,
                                      'Transport': transport_type,
                                      'Distance (Km)': distance })
                
        return random_points

    def save_points_to_csv(self, points_df, file_path):
        if points_df is None:
            return
        
        try:
            points_df.to_csv(file_path, index=False)
            print("Points saved to CSV successfully.")
        except Exception as e:
            print("Error saving points to CSV:", e)

# Main code execution
if __name__ == "__main__":
    generator = DataCreation("Singapore.geojson")

    num_points = 5000

    # Generate random points within the bounds of the boundary data
    transport_probabilities = {'motorcycle': 0.5, 'car': 0.2, 'bike': 0.3}  
    
    # Parallelize point generation
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(generator.generate_random_points_within_bounds, num_points // 4, transport_probabilities) for _ in range(4)]
        random_points = [future.result() for future in futures]

    # Flatten list of lists
    random_points = [point for sublist in random_points for point in sublist]

    # Convert list of dictionaries to GeoDataFrame
    random_points_gdf = gpd.GeoDataFrame(random_points, geometry=gpd.points_from_xy([point['DeliveryLongitude'] for point in random_points], 
                                                                                    [point['DeliveryLatitude'] for point in random_points]),
                                         crs='EPSG:4326')
    
    # Save points to CSV
    if not random_points_gdf.empty:
        generator.save_points_to_csv(random_points_gdf[['Delivery_ID', 'Transport', 'DeliveryLatitude', 'DeliveryLongitude', 
                                              'RestaurantLatitude', 'RestaurantLongitude', 'Distance (Km)']], 
                                              "TestData.csv")

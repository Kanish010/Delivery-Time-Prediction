import folium
import osmnx as ox

def generate_heat_map_with_route(restaurant_location, delivery_location):
    # Create a folium map centered at the restaurant location
    map_center = restaurant_location
    m = folium.Map(location=map_center, zoom_start=12)

    # Add marker for restaurant and delivery location
    folium.Marker(restaurant_location, popup="Restaurant").add_to(m)
    folium.Marker(delivery_location, popup="Delivery Location").add_to(m)

    # Get the street network within the bounding box of the two locations
    G = ox.graph_from_bbox(delivery_location[0], restaurant_location[0], delivery_location[1], restaurant_location[1], network_type='drive')

    # Get the nearest nodes to the restaurant and delivery locations
    restaurant_node = ox.distance.nearest_nodes(G, restaurant_location[0], restaurant_location[1])
    delivery_node = ox.distance.nearest_nodes(G, delivery_location[0], delivery_location[1])

    # Calculate the shortest path between the two locations
    route = ox.distance.shortest_path(G, restaurant_node, delivery_node, weight='length')

    # Convert the route nodes to coordinates
    route_coordinates = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]

    # Add PolyLine for the route
    folium.PolyLine(locations=route_coordinates, color='blue').add_to(m)

    # Estimate time taken based on length of the route and assumed average speed (in km/h)
    route_length = sum(ox.utils_graph.get_route_edge_attributes(G, route, 'length'))
    average_speed_kmh = 30  # Assumed average speed in km/h
    estimated_time_hours = route_length / average_speed_kmh
    estimated_time_minutes = estimated_time_hours * 60

    # Add popup with estimated time
    popup_text = f"Estimated Time: {estimated_time_minutes:.2f} minutes"
    folium.Popup(popup_text).add_to(folium.Marker(delivery_location, popup=popup_text))

    # Save the map to an HTML file or display it
    m.save("heat_map_with_route.html")

def main():
    # Sample delivery location and restaurant location (to be input by the user)
    delivery_location = (1.3196, 103.7525)  # Example coordinates
    restaurant_location = (1.2964, 103.7925)  # Example coordinates

    # Generate heat map with route and estimated time
    generate_heat_map_with_route(restaurant_location, delivery_location)

if __name__ == "__main__":
    main()
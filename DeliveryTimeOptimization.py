import folium
import googlemaps
import polyline

# Google Maps API Key
API_KEY = 'YOUR_API_KEY'

def generate_road_map(restaurant_location, delivery_location):
    # Create a folium map centered at the restaurant location
    map_center = restaurant_location
    m = folium.Map(location=map_center, zoom_start=12)

    # Add marker for restaurant and delivery location
    folium.Marker(restaurant_location, popup="Restaurant").add_to(m)
    delivery_marker = folium.Marker(delivery_location).add_to(m)

    # Calculate directions using Google Maps Directions API
    gmaps = googlemaps.Client(key=API_KEY)
    directions = gmaps.directions(restaurant_location, delivery_location, mode="driving")

    # Extract duration from the directions
    duration_text = directions[0]['legs'][0]['duration']['text']

    # Concatenate popup text
    popup_text = "Delivery Location: {}".format(duration_text)

    # Add delivery duration as popup
    folium.Popup(popup_text).add_to(delivery_marker)

    # Extract the polyline representing the route
    polyline_points = directions[0]['overview_polyline']['points']

    # Decode the polyline points
    decoded_points = polyline.decode(polyline_points)

    # Add the route polyline to the map
    folium.PolyLine(locations=decoded_points, color='blue', weight=5, opacity=0.7, popup="Delivery Route").add_to(m)

    # Save the map to an HTML file or display it
    m.save("Delivery_Route.html")

def main():
    # Sample delivery location and restaurant location (to be input by the user)
    delivery_location = (1.3196, 103.7525)  # Example coordinates
    restaurant_location = (1.2964, 103.7925)  # Example coordinates

    # Generate road map
    generate_road_map(restaurant_location, delivery_location)

if __name__ == "__main__":
    main()
import folium

def generate_heat_map(restaurant_location, delivery_location):
    # Create a folium map centered at the restaurant location
    map_center = restaurant_location
    m = folium.Map(location=map_center, zoom_start=12)

    # Add marker for restaurant and delivery location
    folium.Marker(restaurant_location, popup="Restaurant").add_to(m)
    folium.Marker(delivery_location, popup="Delivery Location").add_to(m)

    # Save the map to an HTML file or display it
    m.save("heat_map.html")

def main():
    # Sample delivery location and restaurant location (to be input by the user)
    delivery_location = (1.3196, 103.7525)  # Example coordinates
    restaurant_location = (1.2964, 103.7925)  # Example coordinates

    # Generate heat map
    generate_heat_map(restaurant_location, delivery_location)

if __name__ == "__main__":
    main()

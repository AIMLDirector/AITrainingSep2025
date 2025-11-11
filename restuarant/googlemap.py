import googlemaps
from pprint import pprint # Pretty-print for better readability

# Replace with your actual API key
API_KEY = "AIzaSyBYdISdp7gEOO1caPxwOW0-Ir5UPkB7lBk"

# Initialize the Google Maps client
gmaps = googlemaps.Client(key=API_KEY)

# Define the query for HSR Layout restaurants
query = "restaurants in HSR Layout, Bengaluru"

# Perform a text search for restaurants
places_result = gmaps.places(query=query)

# Extract and print the restaurant names
if places_result['status'] == 'OK':
    restaurants = places_result['results']
    print(f"Found {len(restaurants)} restaurants in HSR Layout:\n")
    for index, restaurant in enumerate(restaurants):
        print(f"{index + 1}. {restaurant['name']}")
        print(f"   Address: {restaurant.get('formatted_address', 'N/A')}")
        print(f"   Rating: {restaurant.get('rating', 'N/A')}\n")

    # If there are more results, the API provides a `next_page_token`.
    # You would need to handle this to fetch additional pages of results.
    # The `googlemaps.places` function supports pagination with a `page_token` argument.
    if 'next_page_token' in places_result:
        print("More results are available. You can fetch the next page using the 'next_page_token'.")

else:
    print(f"Error fetching places: {places_result['status']}")

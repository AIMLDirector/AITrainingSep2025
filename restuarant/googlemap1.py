from google.maps import places_v1
import os

# Replace with your actual API key
# For enhanced security, consider using the environment variable method
os.environ['GOOGLE_API_KEY'] = 'AIzaSyBYdISdp7gEOO1caPxwOW0-Ir5UPkB7lBk'

# The `google-maps-places` library automatically handles the client setup
# if the GOOGLE_API_KEY environment variable is set.
def search_restaurants_in_hsr(query):
    """Performs a Text Search for restaurants in HSR Layout."""
    try:
        client = places_v1.PlacesClient()

        # Define the request with the query
        request = places_v1.SearchTextRequest(
            text_query=query,
            language_code="en",  # Optional: specify language
            max_result_count=20  # Optional: specify max results per page
        )

        # Define the field mask to request specific data fields
        # This is required by the Places API (New)
        field_mask = [
            "places.display_name",
            "places.formatted_address",
            "places.rating"
        ]

        # Execute the request
        response = client.search_text(request=request, field_mask=field_mask)

        # Print the restaurant details
        if response.places:
            print(f"Found {len(response.places)} restaurants in HSR Layout:\n")
            for index, place in enumerate(response.places):
                print(f"{index + 1}. {place.display_name}")
                print(f"   Address: {place.formatted_address}")
                print(f"   Rating: {place.rating}\n")
        else:
            print("No restaurants found.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage with a more specific query for HSR Layout
query = "restaurants in HSR Layout, Bengaluru"
search_restaurants_in_hsr(query)

from google.maps import places_v1

def search_places():
    client = places_v1.PlacesClient()

    request = places_v1.SearchTextRequest(
        text_query="restaurants in Chennai",
        # NEW way to specify fields
        # The field_mask tells Google which fields you want in the response
        # Without it, you may get a minimal response or an error
        language_code="en"
    )

    response = client.search_text(request=request)

    # Print results
    for place in response.places:
        print(place.display_name.text, "-", place.formatted_address)

search_places()

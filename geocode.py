from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable

# Initialize Nominatim Geocoder with a specific user agent and a longer timeout
geolocator = Nominatim(user_agent="wx_at_destination_app",
                       timeout=5)  # Timeout set to 5 seconds


def get_geocoded_address(address):
    try:
        # Perform geocoding to get latitude and longitude
        location = geolocator.geocode(address)

        if location:
            return location.latitude, location.longitude
        else:
            print("Location could not be geocoded")
    except GeocoderUnavailable:
        print("Geocoder service is unavailable. Please try again later.")

import googlemaps
from dotenv import load_dotenv
import os

from requests.models import LocationParseError

load_dotenv()

gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))

hospitals = gmaps.places_nearby(
    location = (31.5204,74.3587),  # Example coordinates (lahore)
    radius = 5000,
    type = "hospital" 
)

def print_hospital_info(hospitals):
    """Print formatted information about hospitals"""
    if not hospitals:
        print("No hospitals found.")
        return
    
    print(f"\nFound {len(hospitals)} hospitals:")
    print("-" * 50)
    
    for i, hospital in enumerate(hospitals, 1):
        name = hospital.get('name', 'Unknown')
        address = hospital.get('vicinity', 'Address not available')
        rating = hospital.get('rating', 'No rating')
        
        print(f"{i}. {name}")
        print(f"   Address: {address}")
        print(f"   Rating: {rating}")
        
        if 'opening_hours' in hospital:
            is_open = hospital['opening_hours'].get('open_now', 'Unknown')
            print(f"   Open now: {is_open}")
        
        print()


if __name__ == "__main__":
    print_hospital_info(hospitals.get('results', []))
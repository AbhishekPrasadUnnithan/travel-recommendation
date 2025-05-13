import requests
import pandas as pd
from sqlalchemy import create_engine
import time

# Replace this with your actual Google Places API key
API_KEY = "AIzaSyDAc6pSHWoyjIGL_3yM9FPh1ia3rM7EdQM"

# Assign price level based on rating if missing
def map_rating_to_price_level(rating):
    if rating >= 4.5:
        return 4  # Very Expensive
    elif rating >= 4.0:
        return 3  # Expensive
    elif rating >= 3.5:
        return 2  # Moderate
    else:
        return 1  # Inexpensive

# Map price level to estimated price
def map_price_level_to_price(price_level):
    if price_level == 1:
        return 1500
    elif price_level == 2:
        return 2500
    elif price_level == 3:
        return 3500
    elif price_level == 4:
        return 4500
    else:
        return 3000  # Default fallback

# Fetch hotels from Google API using next_page_token for full results
def fetch_all_hotels(city, radius=5000):
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": f"hotels in {city}",
        "radius": radius,
        "key": API_KEY
    }

    hotel_list = []
    page = 1

    while True:
        response = requests.get(base_url, params=params)
        data = response.json()

        results = data.get("results", [])

        for hotel in results:
            name = hotel.get("name")
            rating = hotel.get("rating", 0.0)
            if rating is None:
                rating = 0.0
            address = hotel.get("formatted_address")
            price_level = hotel.get("price_level")
            if price_level is None:
                price_level = map_rating_to_price_level(rating)
            price = map_price_level_to_price(price_level)

            # Add Google Maps link
            place_id = hotel.get("place_id")
            google_maps_link = f"https://www.google.com/maps/place/?q=place_id:{place_id}"

            hotel_list.append({
                "name": name,
                "rating": rating,
                "address": address,
                "price_level": price_level,
                "price": price,
                "city": city,
                "map_link": google_maps_link
            })

        next_token = data.get("next_page_token")
        if not next_token or page >= 3:
            break

        params = {
            "pagetoken": next_token,
            "key": API_KEY
        }
        time.sleep(2)  # Wait for token to activate
        page += 1

    return hotel_list

# Save results to SQLite database
def save_to_db(all_hotels):
    df = pd.DataFrame(all_hotels)
    print("Saving to hotels.db...")
    engine = create_engine("sqlite:///hotels.db")
    df.to_sql("hotels", engine, if_exists="replace", index=False)
    print("Saved successfully!")

# Main logic
if __name__ == "__main__":
    cities = ["Kochi", "Delhi", "Mumbai", "Bangalore", "Chennai", "Hyderabad"]
    all_hotels = []

    for city in cities:
        print(f"Fetching hotels in {city}...")
        hotels = fetch_all_hotels(city)
        all_hotels.extend(hotels)

    save_to_db(all_hotels)
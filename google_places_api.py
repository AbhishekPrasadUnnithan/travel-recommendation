import requests
import pandas as pd
from sqlalchemy import create_engine
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API Key from environment variable
API_KEY = os.getenv("GOOGLE_API_KEY")

# Assign price level based on rating if missing
def map_rating_to_price_level(rating):
    if rating >= 4.5:
        return 4
    elif rating >= 4.0:
        return 3
    elif rating >= 3.5:
        return 2
    else:
        return 1

# Map price level to estimated price
def map_price_level_to_price(price_level):
    return {
        1: 1500,
        2: 2500,
        3: 3500,
        4: 4500
    }.get(price_level, 3000)

# Fetch hotels from Google API
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
            address = hotel.get("formatted_address")
            price_level = hotel.get("price_level") or map_rating_to_price_level(rating)
            price = map_price_level_to_price(price_level)
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
        time.sleep(2)
        page += 1

    return hotel_list

# Save to database
def save_to_db(all_hotels):
    df = pd.DataFrame(all_hotels)
    print("Saving to hotels.db...")
    engine = create_engine("sqlite:///hotels.db")
    df.to_sql("hotels", engine, if_exists="replace", index=False)
    print("Saved successfully!")

# Main
if __name__ == "__main__":
    cities = ["Kochi", "Delhi", "Mumbai", "Bangalore", "Chennai", "Hyderabad"]
    all_hotels = []

    for city in cities:
        print(f"Fetching hotels in {city}...")
        hotels = fetch_all_hotels(city)
        all_hotels.extend(hotels)

    save_to_db(all_hotels)
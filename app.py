import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Set a background image using custom CSS
def set_background():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://wa-uploads.profitroom.com/castellsonclaret/2400x1080/17282996803046_castellsonclaretpoolv1.jpg");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        .block-container {
            background-color: rgba(255, 255, 255, 0.85);
            padding: 2rem;
            border-radius: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Call background setup
set_background()

# Connect to the database
engine = create_engine("sqlite:///hotels.db")

st.title("Hotel Recommendation System")

# Fetch available cities from the database
city_list = pd.read_sql("SELECT DISTINCT city FROM hotels", engine)['city'].tolist()

# Sidebar filters
st.sidebar.header("Filter Options")
city = st.sidebar.selectbox("Choose a City", city_list)
rating_range = st.sidebar.slider("Rating Range", 0.0, 5.0, (3.0, 5.0), step=0.1)

price_level_map = {
    "Inexpensive (₹1000–2000)": 1,
    "Moderate (₹2000–3000)": 2,
    "Expensive (₹3000–4000)": 3,
    "Very Expensive (₹4000+)": 4
}
price_level_choice = st.sidebar.selectbox("Choose Price Level", list(price_level_map.keys()))
selected_price_level = price_level_map[price_level_choice]

# Optional hotel name search
search_name = st.sidebar.text_input("Search by Hotel Name (Optional)")

# Query and filter when the button is clicked
if st.sidebar.button("Find Hotels"):
    query = f"""
        SELECT name, rating, price, price_level, address, map_link
        FROM hotels
        WHERE city = '{city}'
        AND rating BETWEEN {rating_range[0]} AND {rating_range[1]}
        AND price_level = {selected_price_level}
    """
    if search_name:
        query += f" AND name LIKE '%{search_name}%'"
    query += " ORDER BY rating DESC"

    df = pd.read_sql(query, engine)

    if df.empty:
        st.warning("No hotels found matching your criteria.")
    else:
        st.success(f"Found {len(df)} hotels in {city}")

        # Map numeric price_level to text labels
        reverse_price_map = {
            1: "Inexpensive",
            2: "Moderate",
            3: "Expensive",
            4: "Very Expensive"
        }
        df['price_level'] = df['price_level'].map(reverse_price_map)

        # Create clickable Google Maps links, if present
        if 'map_link' in df.columns:
            df['Google Maps'] = df['map_link'].apply(
                lambda x: f'<a href="{x}" target="_blank">View Hotel</a>'
            )
            df = df.drop(columns=['map_link'])
        
        # Drop the raw price column from the display
        if 'price' in df.columns:
            df = df.drop(columns=['price'])
        
        # Display the updated table without average metrics
        st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)

# Footer note
st.markdown("""
    <hr>
    <center>
    <small>Developed by Abhishek P. Unnithan | Powered by Google Places API & Streamlit</small>
    </center>
""", unsafe_allow_html=True)
import pandas as pd
from sqlalchemy import create_engine

# Connect to your database
engine = create_engine("sqlite:///hotels.db")

# Check if 'hotels' table exists and load data
try:
    df = pd.read_sql("SELECT * FROM hotels", engine)
    print("Database loaded successfully!")
    print(df.head())  # Print the first few rows
except Exception as e:
    print("Error reading from hotels.db:", e)
# Hotel Recommendation System

A travel accommodation recommendation system built using *Google Places API, **Streamlit, and **SQLite, designed to help users filter and explore hotels based on **location, **customer ratings, and **price levels*.

---

## Features

- Filter hotels by:
  - City
  - Rating range
  - Price level (Inexpensive, Moderate, Expensive, Very Expensive)
  - Optional hotel name search
- Google Maps link for each hotel
- Price level is displayed in simple text form (e.g., "Moderate")
- Clean and intuitive UI built with Streamlit
- Data stored locally in SQLite using SQLAlchemy

---

## Tech Stack

- Python 3.10
- Streamlit
- SQLite + SQLAlchemy
- Pandas
- Google Places API

---

## Limitations & Assumptions

Due to restrictions of the Google Places API:

- *Actual hotel price values* are *not available* via the API unless the hotel integrates with Google’s booking partners — which is rare.
- The price_level field (0 to 4) is only available for some listings.
- In many cases, even the price_level is missing. Therefore:
  - We estimate price_level based on *user ratings*, as a fallback strategy:
    - Rating ≥ 4.5 → Very Expensive
    - Rating ≥ 4.0 → Expensive
    - Rating ≥ 3.5 → Moderate
    - Else → Inexpensive
- This allows consistent filtering of hotels by *estimated price level*, even when no explicit price data is returned by the API.

> This assumption was made to ensure the app provides useful price filtering and recommendation despite API limitations.

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/AbhishekPrasadUnnithan/travel-recommendation.git
cd travel-recommendation
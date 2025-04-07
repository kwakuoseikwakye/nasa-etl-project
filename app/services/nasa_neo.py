import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from app.utils.logger import logger

load_dotenv()

NASA_API_KEY = os.getenv("NASA_API_KEY")
NEO_WS_URL = "https://api.nasa.gov/neo/rest/v1/feed"

def fetch_neo_data(start_date: str, end_date: str) -> dict:
    logger.info(f"Fetching NEO data from {start_date} to {end_date}")

    params = {
        "api_key": NASA_API_KEY,
        "start_date": start_date,
        "end_date": end_date
    }

    try:
        response = requests.get(NEO_WS_URL, params=params)
        response.raise_for_status()
        data = response.json()
        total = sum(len(v) for v in data["near_earth_objects"].values())
        logger.info(f"Fetched {total} asteroid entries")
        return data
    except requests.exceptions.RequestException as e:
        logger.error(f"NeoWs API request failed: {e}")
        return {}

def get_last_30_days_neo() -> list:
    today = datetime.utcnow().date()
    start_date = today - timedelta(days=30)

    all_asteroids = []

    current = start_date
    while current < today:
        next_chunk = min(current + timedelta(days=6), today)
        data = fetch_neo_data(current.isoformat(), next_chunk.isoformat())

        for date_str, asteroids in data.get("near_earth_objects", {}).items():
            all_asteroids.extend(asteroids)

        current = next_chunk + timedelta(days=1)

    return all_asteroids

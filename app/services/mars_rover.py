import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from app.utils.logger import logger

load_dotenv()

NASA_API_KEY = os.getenv("NASA_API_KEY")
MARS_URL = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"

def fetch_photos_by_date(date: str) -> list:
    params = {
        "earth_date": date,
        "api_key": NASA_API_KEY
    }

    try:
        response = requests.get(MARS_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("photos", [])
    except requests.exceptions.RequestException as e:
        logger.error(f"Mars Rover API request failed for {date}: {e}")
        return []

def get_last_30_days_mars_photos() -> list:
    today = datetime.utcnow().date()
    start_date = today - timedelta(days=30)

    all_photos = []

    for i in range(31):
        date = (start_date + timedelta(days=i)).isoformat()
        logger.info(f"Fetching Mars Rover photos for {date}")
        photos = fetch_photos_by_date(date)
        if photos:
            logger.info(f"Fetched {len(photos)} photos for {date}")
            all_photos.extend(photos)

    return all_photos

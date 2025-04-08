import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from app.utils.logger import logger

load_dotenv()

NASA_API_KEY = os.getenv("NASA_API_KEY")
APOD_URL = "https://api.nasa.gov/planetary/apod"

def fetch_apod_data(start_date: str, end_date: str) -> list:
    logger.info(f"Fetching APOD data from {start_date} to {end_date}")
    
    params = {
        "api_key": NASA_API_KEY,
        "start_date": start_date,
        "end_date": end_date,
    }

    try:
        response = requests.get(APOD_URL, params=params)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Fetched {len(data)} APOD records")
        return data
    except requests.exceptions.RequestException as e:
        logger.error(f"APOD API request failed: {e}")
        return []

def get_last_30_days_apod() -> list:
    today = datetime.utcnow().date()
    thirty_days_ago = today - timedelta(days=30)
    return fetch_apod_data(thirty_days_ago.isoformat(), today.isoformat())

import requests
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any
import os


NASA_API_KEY = os.getenv("NASA_API_KEY")

logger = logging.getLogger(__name__)

class Extractor:
    BASE_URLS = {
        "apod": "https://api.nasa.gov/planetary/apod",
        "neo": "https://api.nasa.gov/neo/rest/v1/feed",
        "mars": "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"
    }

    def __init__(self, api_key: str = NASA_API_KEY):
        self.api_key = api_key

    def fetch_apod(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        logger.info(f"Fetching APOD data from {start_date} to {end_date}")
        params = {
            "api_key": self.api_key,
            "start_date": start_date,
            "end_date": end_date
        }
        response = requests.get(self.BASE_URLS["apod"], params=params)
        response.raise_for_status()
        return response.json()

    def fetch_neo(self, start_date: str, end_date: str) -> Dict[str, Any]:
        logger.info(f"Fetching NEO data from {start_date} to {end_date}")
        params = {
            "api_key": self.api_key,
            "start_date": start_date,
            "end_date": end_date
        }
        response = requests.get(self.BASE_URLS["neo"], params=params)
        response.raise_for_status()
        return response.json()

    def fetch_mars_photos(self, earth_date: str) -> List[Dict[str, Any]]:
        logger.info(f"Fetching Mars Rover photos for {earth_date}")
        params = {
            "api_key": self.api_key,
            "earth_date": earth_date
        }
        response = requests.get(self.BASE_URLS["mars"], params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("photos", [])

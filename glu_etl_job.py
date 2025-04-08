import sys
import os
from dotenv import load_dotenv
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import requests

import pandas as pd
from app.services.extractor import (
    get_last_30_days_apod,
    get_last_30_days_neo,
    get_last_30_days_mars_photos
)
from app.services.transformer import (
    transform_apod_data,
    transform_neo_data,
    transform_mars_photos
)
from app.db.models import Base, Apod, Neo, MarsPhoto

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

DB_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@" \
         f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)

def load_data(df, model):
    session = Session()
    for _, row in df.iterrows():
        session.merge(model(**row.to_dict()))
    session.commit()
    session.close()
    
def analyze_image(image_url: str, service_url: str):
    try:
        response = requests.post(
            f"{service_url}/analyze-image",
            json={"url": image_url},
            timeout=5  # fail fast
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[WARN] Could not analyze image {image_url}: {e}")
        return {
            "width": None,
            "height": None,
            "dominant_color": None
        }

def run_etl():
    logger.info("Running ETL job...")

    apod_raw = get_last_30_days_apod()
    neo_raw = get_last_30_days_neo()
    mars_raw = get_last_30_days_mars_photos()

    apod_df = transform_apod_data(apod_raw)
    neo_df = transform_neo_data(neo_raw)
    mars_df = transform_mars_photos(mars_raw)

    Base.metadata.create_all(bind=engine)

    load_data(apod_df, Apod)
    load_data(neo_df, Neo)
    load_data(mars_df, MarsPhoto)

    logger.info("ETL completed.")

if __name__ == "__main__":
    run_etl()

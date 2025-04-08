from app.db.engine import SessionLocal
from app.db.models import Apod, Neo, MarsPhoto
from sqlalchemy.exc import IntegrityError
import pandas as pd
from app.utils.logger import logger

def load_apod(df: pd.DataFrame):
    session = SessionLocal()
    try:
        logger.info("Loading APOD data...")
        for _, row in df.iterrows():
            record = Apod(
                date=row["date"],
                title=row["title"],
                explanation=row["explanation"],
                image_url=row["image_url"],
                hd_image_url=row["hd_image_url"]
            )
            session.merge(record)
        session.commit()
    except IntegrityError as e:
        logger.error(f"APOD load error: {e}")
        session.rollback()
    finally:
        session.close()

def load_neo(df: pd.DataFrame):
    session = SessionLocal()
    try:
        logger.info("Loading NEO data...")
        for _, row in df.iterrows():
            record = Neo(
                id=row["id"],
                name=row["name"],
                event_date=row["close_approach_date"],
                velocity_kph=row["velocity_kph"],
                miss_distance_km=row["miss_distance_km"],
                diameter_min_km=row["diameter_min_km"],
                diameter_max_km=row["diameter_max_km"],
                is_hazardous=row["is_hazardous"]
            )
            session.merge(record)
        session.commit()
    except IntegrityError as e:
        logger.error(f"NEO load error: {e}")
        session.rollback()
    finally:
        session.close()

def load_mars(df: pd.DataFrame):
    session = SessionLocal()
    try:
        logger.info("Loading Mars photos...")
        for _, row in df.iterrows():
            record = MarsPhoto(
                id=row["id"],
                image_url=row["image_url"],
                earth_date=row["earth_date"],
                camera_name=row["camera_name"],
                rover_name=row["rover_name"]
            )
            session.merge(record)
        session.commit()
    except IntegrityError as e:
        logger.error(f"Mars load error: {e}")
        session.rollback()
    finally:
        session.close()

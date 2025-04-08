import pandas as pd
from datetime import datetime
from app.utils.logger import logger

def transform_apod_data(raw_data: list) -> pd.DataFrame:
    logger.info("Transforming APOD data...")
    df = pd.DataFrame(raw_data)

    df = df[df["media_type"] == "image"]
    df["date"] = pd.to_datetime(df["date"])
    df = df.drop_duplicates(subset=["date"])

    df = df[["date", "title", "explanation", "url", "hdurl"]].copy()
    df.rename(columns={
        "url": "image_url",
        "hdurl": "hd_image_url"
    }, inplace=True)

    return df

def transform_neo_data(raw_data: list) -> pd.DataFrame:
    logger.info("Transforming NEO (asteroid) data...")
    df = pd.DataFrame(raw_data)

    df["close_approach_date"] = df["close_approach_data"].apply(lambda x: x[0]["close_approach_date"] if x else None)
    df["velocity_kph"] = df["close_approach_data"].apply(lambda x: float(x[0]["relative_velocity"]["kilometers_per_hour"]) if x else None)
    df["miss_distance_km"] = df["close_approach_data"].apply(lambda x: float(x[0]["miss_distance"]["kilometers"]) if x else None)

    df["diameter_min_km"] = df["estimated_diameter"].apply(lambda x: x["kilometers"]["estimated_diameter_min"])
    df["diameter_max_km"] = df["estimated_diameter"].apply(lambda x: x["kilometers"]["estimated_diameter_max"])

    df["is_hazardous"] = df["is_potentially_hazardous_asteroid"]

    df = df[[
        "id", "name", "close_approach_date", "velocity_kph", "miss_distance_km",
        "diameter_min_km", "diameter_max_km", "is_hazardous"
    ]].copy()

    df.dropna(subset=["close_approach_date"], inplace=True)
    df["close_approach_date"] = pd.to_datetime(df["close_approach_date"])
    df.drop_duplicates(subset=["id", "close_approach_date"], inplace=True)

    return df

def transform_mars_photos(raw_data: list) -> pd.DataFrame:
    logger.info("Transforming Mars Rover photo data...")
    df = pd.DataFrame(raw_data)

    df["earth_date"] = pd.to_datetime(df["earth_date"])
    df["camera_name"] = df["camera"].apply(lambda x: x["full_name"] if isinstance(x, dict) else None)
    df["rover_name"] = df["rover"].apply(lambda x: x["name"] if isinstance(x, dict) else None)

    df = df[["id", "img_src", "earth_date", "camera_name", "rover_name"]].copy()
    df.rename(columns={"img_src": "image_url"}, inplace=True)

    df.drop_duplicates(subset=["id"], inplace=True)
    return df


def integrate_datasets(apod_df: pd.DataFrame, neo_df: pd.DataFrame, mars_df: pd.DataFrame) -> dict:
    logger.info("Integrating datasets...")

    apod_df["date"] = pd.to_datetime(apod_df["date"])
    neo_df["close_approach_date"] = pd.to_datetime(neo_df["close_approach_date"])
    mars_df["earth_date"] = pd.to_datetime(mars_df["earth_date"])

    apod = apod_df.rename(columns={"date": "event_date"})
    neo = neo_df.rename(columns={"close_approach_date": "event_date"})
    mars = mars_df.rename(columns={"earth_date": "event_date"})

    merged_df = pd.merge(apod, neo, on="event_date", how="outer", suffixes=("_apod", "_neo"))
    merged_df = pd.merge(merged_df, mars, on="event_date", how="outer")

    logger.info(f"Merged dataset contains {len(merged_df)} records")

    return {
        "merged": merged_df,
        "apod": apod_df,
        "neo": neo_df,
        "mars": mars_df
    }

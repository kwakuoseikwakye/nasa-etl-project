from fastapi import FastAPI
from app.utils.logger import logger
from app.services.nasa_apod import get_last_30_days_apod
from app.services.nasa_neo import get_last_30_days_neo
from app.services.mars_rover import get_last_30_days_mars_photos
from app.services.transformer import transform_apod_data, transform_neo_data, transform_mars_photos
from app.services.transformer import integrate_datasets

app = FastAPI(title="NASA ETL Microservice")

@app.get("/")
def read_root():
    logger.info("Health check endpoint called")
    return {"message": "NASA ETL Microservice is running!"}

@app.get("/apod")
def get_apod_data():
    data = get_last_30_days_apod()
    return {"count": len(data), "sample": data[:1]}

@app.get("/neo")
def get_neo_data():
    data = get_last_30_days_neo()
    return {"count": len(data), "sample": data[:1]}

@app.get("/mars")
def get_mars_data():
    data = get_last_30_days_mars_photos()
    return {"count": len(data), "sample": data[:1]}

@app.get("/transform")
def transform_all_data():
    apod_raw = get_last_30_days_apod()
    neo_raw = get_last_30_days_neo()
    mars_raw = get_last_30_days_mars_photos()

    apod_df = transform_apod_data(apod_raw)
    neo_df = transform_neo_data(neo_raw)
    mars_df = transform_mars_photos(mars_raw)

    return {
        "apod_sample": apod_df.head(1).to_dict(orient="records"),
        "neo_sample": neo_df.head(1).to_dict(orient="records"),
        "mars_sample": mars_df.head(1).to_dict(orient="records"),
    }
    
@app.get("/integrated")
def get_integrated_data():
    apod_raw = get_last_30_days_apod()
    neo_raw = get_last_30_days_neo()
    mars_raw = get_last_30_days_mars_photos()

    apod_df = transform_apod_data(apod_raw)
    neo_df = transform_neo_data(neo_raw)
    mars_df = transform_mars_photos(mars_raw)

    integrated = integrate_datasets(apod_df, neo_df, mars_df)
    merged_sample = integrated["merged"].head(2).fillna("NA").to_dict(orient="records")

    return {
        "sample_merged": merged_sample,
        "record_count": len(integrated["merged"])
    }
from fastapi import FastAPI
from app.utils.logger import logger
from app.services.nasa_apod import get_last_30_days_apod
from app.services.nasa_neo import get_last_30_days_neo

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
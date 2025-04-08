from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services.analyzer import analyze_image_from_url

app = FastAPI()

class ImageInput(BaseModel):
    url: str

@app.post("/analyze-image")
def analyze(image_input: ImageInput):
    try:
        result = analyze_image_from_url(image_input.url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

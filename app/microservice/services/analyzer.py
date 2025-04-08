import requests
from PIL import Image
from io import BytesIO
import numpy as np
from collections import Counter

def get_dominant_color(image):
    img = image.convert('RGB')
    small_img = img.resize((50, 50))  # speed up
    pixels = list(small_img.getdata())
    most_common = Counter(pixels).most_common(1)
    return most_common[0][0]  # RGB tuple

def analyze_image_from_url(url: str):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    width, height = image.size
    dominant_color = get_dominant_color(image)
    return {
        "width": width,
        "height": height,
        "dominant_color": dominant_color
    }

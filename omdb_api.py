import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OMDB_API_KEY")
BASE_URL = "https://www.omdbapi.com/"

def fetch_movie_data(title: str):
    params = {
        "apikey": API_KEY,
        "t": title,
        "plot": "full"
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    data = response.json()

    if data.get("Response") == "False":
        raise ValueError(data.get("Error"))

    return data

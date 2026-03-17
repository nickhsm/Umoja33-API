from fastapi import FastAPI
from .models.weather_post import Weather

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/weather")
def post_weather_data(weather: Weather):
    return weather.sensors

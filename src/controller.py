from typing import Annotated

from fastapi import FastAPI
from sqlmodel import Session, select

from .database.orm.weather import DataPoint, WeatherStation
from .database.database_connection import engine

from .models.weather_post import Weather

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/weather")
def post_weather_data(weather: Weather):
    # Get weatherstation_id
    with Session(engine) as session:
        statement = select(WeatherStation).where(WeatherStation.station_id == weather.station_id)
        weatherstation_id = session.exec(statement)

    data = DataPoint(
            temperature=weather.sensors.temperature,
            humidity=weather.sensors.humidity,
            wind_speed=weather.sensors.wind_speed,
            wind_direction=weather.sensors.wind_direction,
            precipitation=weather.sensors.precipitation,
            timestamp=weather.timestamp,
            weatherstation_id=weatherstation_id
            )

    with Session(engine) as session:
        session.add(data)

    return {"Status": "success"}

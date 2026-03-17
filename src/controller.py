from typing import Annotated

from fastapi import FastAPI
from sqlmodel import Session, select

from .models.register_weatherstation import RegisterWeatherStation

from .database.orm.weather import DataPoint, WeatherStation
from .database.database_connection import engine

from .models.weather_post import Weather

app = FastAPI()



@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/register/weatherstation")
def register_weatherstation(weatherStation: RegisterWeatherStation):
    print(weatherStation.station_id)
    weatherStation = WeatherStation(
            station_id=weatherStation.station_id,
            )

    with Session(engine) as session:
        session.add(weatherStation)
        session.commit()

    return {"Status": "success"}


@app.post("/weather")
def post_weather_data(weather: Weather):
    # Get weatherstation_id
    with Session(engine) as session:
        statement = select(WeatherStation).where(WeatherStation.station_id == weather.station_id)
        weatherstation_result = session.exec(statement)
        list_result = weatherstation_result.all()
        if list_result == []:
            return {"Status": "You must first register"}

    data = DataPoint(
            temperature=weather.sensors.temperature,
            humidity=weather.sensors.humidity,
            wind_speed=weather.sensors.wind_speed,
            wind_direction=weather.sensors.wind_direction,
            precipitation=weather.sensors.precipitation,
            timestamp=weather.timestamp,
            weatherstation_id=list_result[0].station_id
            )

    with Session(engine) as session:
        session.add(data)
        session.commit()

    return {"Status": "success"}

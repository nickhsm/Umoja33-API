from typing import Annotated, List

from fastapi import FastAPI
from sqlmodel import Session, select

from .models.register_weatherstation import RegisterWeatherStation

from .database.orm.weather import DataPoint, WeatherStation
from .database.database_connection import engine

from .models.weather_post import Weather, Sensors

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/weather", response_model=List[Weather])
def get_all_weather_data():
    with Session(engine) as session:
        statement = select(DataPoint)
        results = session.exec(statement).all()

        statement = select(WeatherStation)
        results_WS = session.exec(statement).all()

        # Create a map of id -> station_id
        ws_map = {ws.id: ws.station_id for ws in results_WS}

        weather_data = []
        for point in results:
            station_id = ws_map[point.id]

            weather_data.append(Weather(
                station_id=str(station_id),
                timestamp=point.timestamp,
                sensors=Sensors(
                    temperature=point.temperature,
                    humidity=point.humidity,
                    wind_speed=point.wind_speed,
                    wind_direction=point.wind_direction,
                    precipitation=point.precipitation
                )
            ))
        return weather_data

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
    weatherstation_id = None
    with Session(engine) as session:
        statement = select(WeatherStation).where(WeatherStation.station_id == weather.station_id)
        results = session.exec(statement).all()
        if not results:
            return {"Status": "You must first register"}
        weatherstation_id = results[0].station_id

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
        session.commit()

    return {"Status": "success"}

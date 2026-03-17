from pydantic import BaseModel


class Sensors(BaseModel):
    temperature: float
    humidity: float
    wind_speed: float
    wind_direction: int



class Weather(BaseModel):
    station_id: str
    sensors: Sensors
    timestamp: str

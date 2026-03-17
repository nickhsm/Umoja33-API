from pydantic import BaseModel


class RegisterWeatherStation(BaseModel):
    station_id: str

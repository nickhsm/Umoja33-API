from datetime import datetime
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
from typing_extensions import List


class WeatherStation(SQLModel, table=True):
    id: Optional[int] | None = Field(default=None, primary_key=True)
    station_id: str
    dataPoints: List["DataPoint"] = Relationship(back_populates="weatherstation")

class DataPoint(SQLModel, table=True):
    id: Optional[int] | None = Field(default=None, primary_key=True)
    temperature: float
    humidity: float
    wind_speed: float
    wind_direction: int
    precipitation: int
    timestamp: datetime
    weatherstation_id: int = Field(foreign_key="weatherstation.id")
    weatherstation: WeatherStation = Relationship(back_populates="dataPoints")

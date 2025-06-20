from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime
from geoalchemy2 import Geometry
from sqlalchemy import Column
# Community Areas SQL Model

class CommunityAreas(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    the_geom: Optional[object] = Field(
        sa_column=Column(Geometry(geometry_type="MULTIPOLYGON", srid=4326))
    )
    area_id: Optional[int] = Field(default=None, index=True, unique=True)
    name: str = Field(index=True)
    # shape_area: Optional[int] = Field(default=None)
    # shape_len: Optional[float] = Field(default=None)
    total_violent_crimes: Optional[int] = Field(default=None)
    total_nonviolent_crimes: Optional[int] = Field(default=None)
    total_population: Optional[int] = Field(default=None)
    total_crimes: Optional[int] = Field(default=None)
    crime_rate: Optional[float] = Field(default=None)
    violent_crime_rate: Optional[float] = Field(default=None)
    nonviolent_crime_rate: Optional[float] = Field(default=None)
    crime_percentile: Optional[float] = Field(default=None)
    # Back-reference to related crime records
    crimes: List["CrimeRates"] = Relationship(back_populates="community")

# Crime Rates SQL Model 
class CrimeRates(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Core details
    crime_id: Optional[int] = Field(default=None, index=True)
    case_number: Optional[str] = Field(default=None, index=True)
    date: Optional[datetime] = Field(default=None, index=True)
    # block: Optional[str] = Field(default=None)
    iucr: Optional[str] = Field(default=None)
    primary_type: Optional[str] = Field(default=None, index=True)
    # description: Optional[str] = Field(default=None)
    # location_description: Optional[str] = Field(default=None)

    # Area info
    # beat: Optional[int] = Field(default=None)
    # district: Optional[int] = Field(default=None)
    # ward: Optional[int] = Field(default=None)
    fbi_code: Optional[str] = Field(default=None)

    # Coordinates
    # x_coordinate: Optional[float] = Field(default=None)
    # y_coordinate: Optional[float] = Field(default=None)
    year: Optional[int] = Field(default=None)
    latitude: Optional[float] = Field(default=None)
    longitude: Optional[float] = Field(default=None)

    # Location string (e.g., POINT (-87.6278 41.8819))
    # location: Optional[str] = Field(default=None)

    # Status
    arrest: Optional[bool] = Field(default=None)
    domestic: Optional[bool] = Field(default=None)
    # updated_on: Optional[datetime] = Field(default=None)

    # Community Area (foreign key)
    community_area: Optional[int] = Field(default=None, foreign_key="communityareas.area_id")
    community: Optional["CommunityAreas"] = Relationship(back_populates="crimes")
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime
# Community Areas SQL Model

class CommunityAreas(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    # Back-reference to related crime records
    crimes: List["CrimeRates"] = Relationship(back_populates="community")

# Crime Rates SQL Model 
class CrimeRates(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Core details
    case_number: Optional[str] = Field(default=None, index=True)
    date: Optional[datetime] = Field(default=None, index=True)
    block: Optional[str] = Field(default=None)
    iucr: Optional[str] = Field(default=None)
    primary_type: Optional[str] = Field(default=None, index=True)
    description: Optional[str] = Field(default=None)
    location_description: Optional[str] = Field(default=None)

    # Area info
    beat: Optional[int] = Field(default=None)
    district: Optional[int] = Field(default=None)
    ward: Optional[int] = Field(default=None)
    fbi_code: Optional[str] = Field(default=None)

    # Coordinates
    x_coordinate: Optional[float] = Field(default=None)
    y_coordinate: Optional[float] = Field(default=None)
    latitude: Optional[float] = Field(default=None)
    longitude: Optional[float] = Field(default=None)

    # Location string (e.g., POINT (-87.6278 41.8819))
    location: Optional[str] = Field(default=None)

    # Status
    arrest: Optional[bool] = Field(default=None)
    domestic: Optional[bool] = Field(default=None)
    updated_on: Optional[datetime] = Field(default=None)

    # Community Area (foreign key)
    community_area: Optional[int] = Field(default=None, foreign_key="communityareas.id")
    community: Optional["CommunityAreas"] = Relationship(back_populates="crimes")
from datetime import datetime
from typing import Literal, Annotated, Optional
from uuid import uuid4

from pydantic import BaseModel, field_validator, Field


# Base properties for Star schema
class StarBase(BaseModel):
    name: str
    right_ascension: Annotated[float, Field(ge=0, le=360)]
    declination: Annotated[float, Field(ge=-90, le=90)]
    diameter: Optional[float]
    mass: Optional[float]
    visible_size: Optional[float]
    distance: Optional[float]
    spectral_class: Optional[str]
    absolute_magnitude: Optional[float]
    constellation_id: Optional[str]


class StarCreate(StarBase):
    ...

# Properties for star in storage
class StarInStorage(StarBase):
    id: str = str(uuid4())


class StarUpdate(StarInStorage):
    ...


# Properties to return to client
class Star(StarInStorage):
    ...


class StarFilter(BaseModel):
    filter_by: Literal['constellation_id', 'spectral_class', 'diameter', 'mass', 'visible_size', 'distance',
                       'absolute_magnitude'] = 'spectral_class'
    filter_string: str | None = ""
    filter_range: tuple[float, float] | None = (0, 1)

    @field_validator('filter_range')
    def is_valid_range(cls, v: tuple[float, float]) -> tuple[float, float]:
        if v[0] >= v[1]:
            raise ValueError('Invalid range')
        return v


class EarthPosition(BaseModel):
    latitude: float
    longitude: float
    timestamp: float | None = datetime.now().timestamp()

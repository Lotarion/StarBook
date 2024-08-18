from uuid import uuid4

from pydantic import BaseModel


# Base properties for Constellation schema
class ConstellationBase(BaseModel):
    name: str


class ConstellationCreate(ConstellationBase):
    ...


class ConstellationInStorage(ConstellationBase):
    id: str = str(uuid4())


class ConstellationUpdate(ConstellationInStorage):
    ...


# For returning to client
class Constellation(ConstellationInStorage):
    ...

from typing import Annotated

from pydantic import BaseModel, Field


class PaginationBase(BaseModel):
    page: Annotated[int, Field(ge=0)] = 0
    per_page: Annotated[int, Field(gt=0)] = 10
    sorting_parameter: str = 'name'
    sorting_direction: str = 'ascending'


class PaginatedOutput(BaseModel):
    total_objects: Annotated[int, Field(ge=0)]
    objects: list

from fastapi import APIRouter, Depends

from app.crud import star_storage
from app.schemas import Star, StarCreate, StarUpdate, PaginationBase, StarFilter, EarthPosition, PaginatedOutput
from .deps import get_filtering_params

router = APIRouter()


@router.get("/", status_code=200, response_model=PaginatedOutput)
def read_stars(
        pagination: PaginationBase = Depends(),
):
    return star_storage.get_all(pagination)


@router.get("/by_name/", status_code=200, response_model=PaginatedOutput)
def read_stars_by_name(
        name: str,
        pagination: PaginationBase = Depends(),
):
    return star_storage.get_by_name(name, pagination)


@router.get("/filtered/", status_code=200, response_model=PaginatedOutput)
def read_all_stars_by_filter(
        filtering: StarFilter = Depends(get_filtering_params),
        pagination: PaginationBase = Depends(),
):
    return star_storage.get_stars_by_filter(filtering, pagination)


@router.get("/visible/", status_code=200, response_model=PaginatedOutput)
def read_all_stars_visible(
        position: EarthPosition = Depends(),
        pagination: PaginationBase = Depends(),
):
    return star_storage.get_stars_visible(position, pagination)


@router.get("/{star_id}", status_code=200, response_model=Star)
def read_star(
        star_id: str
):
    return star_storage.get_one(obj_id=star_id)


@router.post("/", status_code=201, response_model=Star)
def create_star(
        star_in: StarCreate
):
    star = star_storage.create(star_in)
    return star


@router.put("/", status_code=200, response_model=Star)
def update_star(
        star_in: StarUpdate
):
    star = star_storage.update(obj_in=star_in)
    return star


@router.delete("/{star_id}", status_code=200, response_model=Star)
def delete_star(
        star_id: str
):
    return star_storage.delete(obj_id=star_id)

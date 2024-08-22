from fastapi import APIRouter, Depends

from app.crud import constellation_storage
from app.schemas import Constellation, ConstellationCreate, ConstellationUpdate, PaginationBase, PaginatedOutput

router = APIRouter()


@router.get("/", status_code=200, response_model=PaginatedOutput)
def read_constellations():
    """
    Retrieve a page from the list of constellations
    """
    return constellation_storage.get_all()


@router.get("/{constellation_id}/", status_code=200, response_model=Constellation)
def read_constellation(
    constellation_id: str
):
    return constellation_storage.get_one(obj_id=constellation_id)


@router.post("/", status_code=201, response_model=Constellation)
def create_constellation(
        constellation_in: ConstellationCreate
):
    return constellation_storage.create(constellation_in)


@router.put("/", status_code=200, response_model=Constellation)
def update_constellation(
        constellation_in: ConstellationUpdate
):
    return constellation_storage.update(obj_in=constellation_in)


@router.delete("/{constellation_id}/", status_code=200, response_model=Constellation)
def delete_constellation(
        constellation_id: str
):
    return constellation_storage.delete(constellation_id)

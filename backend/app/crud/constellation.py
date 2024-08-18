from app.schemas import ConstellationInStorage
from app.crud import BaseStorage


class ConstellationStorage(BaseStorage):
    DATA_KEY = "constellations"

    def create(self, constellation_in):
        new_obj = ConstellationInStorage.parse_obj(constellation_in.model_dump())
        return self._add_object_to_storage(new_obj)


constellation_storage = ConstellationStorage()

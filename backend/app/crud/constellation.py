import json

from fastapi import HTTPException

from app.core.config import settings
from app.schemas import ConstellationInStorage
from app.crud import BaseStorage


class ConstellationStorage(BaseStorage):
    DATA_KEY = "constellations"

    def create(self, constellation_in):
        new_obj = ConstellationInStorage.model_validate(constellation_in.model_dump())
        return self._add_object_to_storage(new_obj)

    def delete(self, obj_id):
        with open(self.storage_file) as storage_file:
            data = json.load(storage_file)
        obj_index = self._find_index_in_list(obj_id, data[self.DATA_KEY])
        if obj_index != -1:
            deleted_obj = data[self.DATA_KEY].pop(obj_index)
            for star in data[settings.STARS_DATA_KEY]:
                if not star['constellation_id']:
                    continue
                if star['constellation_id'] == deleted_obj['id']:
                    star['constellation_id'] = None
            with open(self.storage_file, 'w') as storage_file:
                json.dump(data, storage_file)
            return deleted_obj
        else:
            raise HTTPException(status_code=404, detail="The specified object doesn't exist")


constellation_storage = ConstellationStorage()

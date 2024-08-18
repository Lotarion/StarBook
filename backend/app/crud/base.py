import json

from fastapi import HTTPException

from app.core.config import ROOT, settings
from app.schemas import PaginationBase, PaginatedOutput

class BaseStorage:
    DATA_KEY: str

    def __init__(self):
        self.storage_file = ROOT / settings.STORAGE_FILE_NAME

    @staticmethod
    def _find_index_in_list(id_in, list_in):
        object_index = -1
        for obj in list_in:
            if obj['id'] == id_in:
                object_index = list_in.index(obj)
        return object_index

    def _add_object_to_storage(self, obj_in):
        with open(self.storage_file) as storage_file:
            data = json.load(storage_file)
        data[self.DATA_KEY].append(obj_in.model_dump())
        with open(self.storage_file, 'w') as storage_file:
            json.dump(data, storage_file)
        return obj_in.model_dump()

    @staticmethod
    def _paginate_list(list_in: list, pagination: PaginationBase):
        start = pagination.page * pagination.per_page
        end = start + pagination.per_page

        list_out = sorted(list_in, key=lambda d: d[pagination.sorting_parameter],
                          reverse=pagination.sorting_direction == 'descending')

        return PaginatedOutput.parse_obj({"total_objects": len(list_in), "objects": list_out[start:end]})

    def get_all(self, pagination: PaginationBase):
        with open(self.storage_file) as storage_file:
            data = json.load(storage_file)
        list_of_objects = data[self.DATA_KEY]

        return self._paginate_list(list_of_objects, pagination)

    def get_one(self, obj_id: str):
        with open(self.storage_file) as storage_file:
            data = json.load(storage_file)
        for obj in data[self.DATA_KEY]:
            if obj['id'] == obj_id:
                return obj
        raise HTTPException(status_code=404, detail="The specified object doesn't exist")

    def get_by_name(self, obj_name: str, pagination: PaginationBase):
        with open(self.storage_file) as storage_file:
            data = json.load(storage_file)
        results = []
        for obj in data[self.DATA_KEY]:
            if obj_name in obj['name']:
                results.append(obj)
        if len(results) > 0:
            return self._paginate_list(results, pagination)
        else:
            raise HTTPException(status_code=404, detail="No objects with the specified name were found")

    def create(self, obj_in):
        ...

    def update(self, obj_in):
        with open(self.storage_file) as storage_file:
            data = json.load(storage_file)
        obj = obj_in.model_dump()
        obj_index = self._find_index_in_list(obj['id'], data[self.DATA_KEY])
        if obj_index != -1:
            data[self.DATA_KEY][obj_index] = obj
            with open(self.storage_file, 'w') as storage_file:
                json.dump(data, storage_file)
            return obj
        else:
            raise HTTPException(status_code=404, detail="The specified object doesn't exist")

    def delete(self, obj_id):
        with open(self.storage_file) as storage_file:
            data = json.load(storage_file)
        obj_index = self._find_index_in_list(obj_id, data[self.DATA_KEY])
        if obj_index != -1:
            deleted_obj = data[self.DATA_KEY].pop(obj_index)
            with open(self.storage_file, 'w') as storage_file:
                json.dump(data, storage_file)
            return deleted_obj
        else:
            raise HTTPException(status_code=404, detail="The specified object doesn't exist")

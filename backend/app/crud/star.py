import json
from datetime import datetime, timezone
from math import sin, cos, asin

from app.core.config import settings
from app.crud import BaseStorage
from app.schemas import StarInStorage, StarFilter, EarthPosition, PaginationBase


class StarStorage(BaseStorage):
    DATA_KEY = settings.STARS_DATA_KEY

    def create(self, star_in):
        new_obj = StarInStorage.model_validate(star_in.model_dump())
        return self._add_object_to_storage(new_obj)

    def get_stars_by_filter(self, filters: StarFilter, pagination: PaginationBase):
        with open(self.storage_file) as storage_file:
            data = json.load(storage_file)
        results = []

        if filters.filter_by in ['constellation_id', 'spectral_class']:
            for star in data[self.DATA_KEY]:
                if star[filters.filter_by] == filters.filter_string:
                    results.append(star)
        else:
            for star in data[self.DATA_KEY]:
                if filters.filter_range[0] < star[filters.filter_by] < filters.filter_range[1]:
                    results.append(star)

        return self._paginate_list(results, pagination)

    @staticmethod
    def _days_since_j2000(dt: datetime) -> float:
        seconds = (dt - datetime(2000, 1, 1, 12, tzinfo=timezone.utc)).total_seconds()
        return seconds / 3600 / 24

    @staticmethod
    def _local_sidereal_time(dt: datetime, long: float) -> float:
        days = star_storage._days_since_j2000(dt)
        ut = dt.hour + dt.minute / 60 + dt.second / 3600

        lst = 100.46 + 0.985647 * days + long + 15 * ut

        while lst < 0:
            lst += 360

        while lst > 360:
            lst -= 360

        return lst

    def get_stars_visible(self, position: EarthPosition, pagination: PaginationBase):
        with open(self.storage_file) as storage_file:
            data = json.load(storage_file)
        results = []

        time = datetime.fromtimestamp(position.timestamp, tz=timezone.utc)
        lst = self._local_sidereal_time(time, position.longitude)
        for star in data[self.DATA_KEY]:
            hour_angle = lst - star['right_ascension']
            sin_altitude = (sin(star['declination']) * sin(position.latitude) +
                            cos(star['declination']) * cos(position.latitude) * cos(hour_angle))
            if asin(sin_altitude) > 0:
                results.append(star)

        return self._paginate_list(results, pagination)


star_storage = StarStorage()

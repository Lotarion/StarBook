from typing import Literal

from fastapi import Query

from app.schemas import PaginationBase, StarFilter


def get_pagination_params(
        p: PaginationBase = Query()
):
    return {"page": p.page,
            "per_page": p.per_page,
            'sorting_parameter': p.sorting_parameter,
            'sorting_direction': p.sorting_direction}


FILTER_PARAMS = Literal['constellation_id', 'spectral_class', 'diameter', 'mass', 'visible_size', 'distance',
                        'absolute_magnitude']


def get_filtering_params(
        filter_by: FILTER_PARAMS = Query(),
        filter_string: str = Query(default="string"),
        filter_range: tuple[float, float] = Query(default=(0, 1)),
):
    filtering = StarFilter.parse_obj(
        {'filter_by': filter_by, 'filter_string': filter_string, 'filter_range': filter_range})

    return filtering

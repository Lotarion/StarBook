from typing import Literal

from fastapi import Query

from app.schemas import StarFilter

FILTER_PARAMS = Literal['constellation_id', 'spectral_class', 'diameter', 'mass', 'visible_size', 'distance',
                        'absolute_magnitude']


def get_filtering_params(
        filter_by: FILTER_PARAMS = Query(default='spectral_class'),
        filter_string: str = Query(default="string"),
        filter_range: tuple[float, float] = Query(default=(0, 1)),
):
    filtering = StarFilter.model_validate(
        {'filter_by': filter_by, 'filter_string': filter_string, 'filter_range': filter_range})

    return filtering

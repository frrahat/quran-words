import pytest

from server.utils import get_next_prev_paginations


@pytest.mark.parametrize('current_offset, current_pagesize, count, expected_prev_pagination, expected_next_pagination', [
    (0, 0, 10, {}, {'offset': 0, 'pagesize': 0}),
    (0, 0, 0, {}, {}),
    (0, 5, 10, {}, {'offset': 5, 'pagesize': 5}),
    (3, 5, 10, {'offset': 0, 'pagesize': 3}, {'offset': 8, 'pagesize': 3}),
    (3, 5, 12, {'offset': 0, 'pagesize': 3}, {'offset': 8, 'pagesize': 5}),
    (3, 5, 13, {'offset': 0, 'pagesize': 3}, {'offset': 8, 'pagesize': 5}),
    (3, 5, 8, {'offset': 0, 'pagesize': 3}, {}),
    (5, 5, 8, {'offset': 0, 'pagesize': 5}, {}),
])
def test_get_next_prev_paginations_gives_expected_output(current_offset,
                                                         current_pagesize,
                                                         count,
                                                         expected_prev_pagination,
                                                         expected_next_pagination):
    prev_pagination, next_pagination = get_next_prev_paginations(
        current_offset, current_pagesize, count)

    assert prev_pagination == expected_prev_pagination
    assert next_pagination == expected_next_pagination

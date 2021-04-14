from typing import Optional
from fastapi import Query


def pagination_parameters(offset: Optional[int] = Query(0, ge=0),
                          pagesize: Optional[int] = Query(10, gt=0)):
    return {
        'offset': offset,
        'pagesize': pagesize,
    }

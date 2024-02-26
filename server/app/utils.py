from typing import Dict, Optional

from fastapi import Request


def get_next_prev_paginations(current_offset: int, current_pagesize: int, count: int):

    prev_pagination = {}
    next_pagination = {}

    if current_offset > 0:
        prev_pagination["offset"] = max(0, current_offset - current_pagesize)
        prev_pagination["pagesize"] = min(current_pagesize, current_offset)

    next_offset = current_offset + current_pagesize

    if next_offset < count:
        next_pagination["offset"] = next_offset
        next_pagination["pagesize"] = min(current_pagesize, count - next_offset + 1)

    return prev_pagination, next_pagination


def get_pagination_response(
    request: Request, count: int, additional_query_string: str = "", limit: int = 10
) -> Dict[str, Optional[str]]:

    current_offset = int(request.query_params.get("offset", 0))
    current_pagesize = int(request.query_params.get("pagesize", limit))

    prev_pagination, next_pagination = get_next_prev_paginations(
        current_offset, current_pagesize, count
    )

    additional_query_params = additional_query_string.split("&")
    non_none_query_params = list(
        filter(
            lambda param: len(param) > 0 and not param.endswith("=None"),
            additional_query_params,
        )
    )
    additional_query_string = (
        f"&{'&'.join(non_none_query_params)}" if non_none_query_params else ""
    )

    url = request.url.path

    return {
        "previous": (
            f"{url}?offset={prev_pagination['offset']}"
            f"&pagesize={prev_pagination['pagesize']}{additional_query_string}"
            if prev_pagination
            else None
        ),
        "next": (
            f"{url}?offset={next_pagination['offset']}"
            f"&pagesize={next_pagination['pagesize']}{additional_query_string}"
            if next_pagination
            else None
        ),
    }

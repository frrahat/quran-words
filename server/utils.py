from typing import Dict, Optional
import urllib.parse

from fastapi import Request


def get_pagination_response(
        request: Request,
        count: int,
        additional_query_string: Optional[str] = None,
        limit: int = 10) -> Dict[str, Optional[str]]:

    current_offset = int(request.query_params.get('offset', 0))
    current_pagesize = int(request.query_params.get('pagesize', limit))

    prev_offset = max(0, current_offset - current_pagesize)
    prev_pagesize = min(current_pagesize, current_offset)

    next_offset = current_offset + current_pagesize
    next_pagesize = min(current_pagesize, count - next_offset + 1)

    additional_query_string = f'&{additional_query_string}' if additional_query_string else ''

    url = urllib.parse.urljoin(str(request.base_url), request.url.path)

    return {
        'previous': f'{url}?offset={prev_offset}&pagesize={prev_pagesize}{additional_query_string}'
        if current_offset > 0 else None,
        'next': f'{url}?offset={next_offset}&pagesize={next_pagesize}{additional_query_string}'
        if next_offset < count else None,
    }

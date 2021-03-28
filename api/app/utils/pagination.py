from typing import Generic, List, Optional, TypeVar, Union

from fastapi import Request
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar('T')

class PageLinks(BaseModel):
    base: str
    self: str
    next: Optional[str]
    prev: Optional[str]


class Page(GenericModel, Generic[T]):
    links: PageLinks
    total: int
    start: int
    limit: int
    size: int
    items: List[T]


def get_base_url(request: Request):
    return str(request.url.remove_query_params(keys=["offset", "limit"]))


def get_next_url(request: Request, offset: int, limit: int, total: int) -> Union[None, str]:
    if offset + limit >= total or limit == -1: return None
    return str(request.url.include_query_params(limit=limit, offset=offset+limit))


def get_prev_url(request: Request, offset: int, limit: int) -> Union[None, str]:
    if offset <= 0: return None
    if offset - limit <= 0:
        return str(request.url.remove_query_params(keys=["offset"]))
    return str(request.url.include_query_params(limit=limit, offset=offset - limit))

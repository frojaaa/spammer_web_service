from typing import Annotated
from enum import Enum, StrEnum

from .schemas import CommonParams

from fastapi import Query


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ProxyProtocol(StrEnum):
    http = 'http'
    socks4 = 'socks4'
    socks5 = 'socks5'


def common_parameters(limit: Annotated[int, Query(gt=0)] = 100, offset: Annotated[int, Query(ge=0)] = 0) -> CommonParams:
    return CommonParams(limit=limit, offset=offset)

from fastapi import APIRouter, Depends, status

from typing import Annotated

from loguru import logger

from .service import ProxiesService
from .schemas import Proxy, ProxyCreate
from db import SessionLocal
from ..dependencies import common_parameters
from ..schemas import CommonParams

router = APIRouter(prefix='/proxies', tags=['proxies'], responses={404: {"description": "Not found"}})
CommonsDep = Annotated[CommonParams, Depends(common_parameters)]


def get_proxies_service() -> ProxiesService:
    db = SessionLocal()
    service = ProxiesService(db)
    try:
        yield service
    finally:
        db.close()


@router.get('/', response_model=list[Proxy])
def read_proxies(
        commons: CommonsDep,
        service: ProxiesService = Depends(get_proxies_service)
) -> list[Proxy]:
    proxies = service.get_proxies(commons.limit, commons.offset)
    return proxies


@router.delete('/delete/{proxy_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_proxy(proxy_id: int, service: ProxiesService = Depends(get_proxies_service)):
    service.delete_proxy(proxy_id)


@logger.catch(BaseException)
@router.post('/create', response_model=list[Proxy], status_code=status.HTTP_201_CREATED)
def create_proxies(proxies: set[ProxyCreate], service: ProxiesService = Depends(get_proxies_service)):
    return service.create_proxies(proxies)

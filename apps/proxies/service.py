from loguru import logger
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from .models import Proxy
from .schemas import ProxyCreate
from ..dependencies import Singleton


class ProxiesService(metaclass=Singleton):
    def __init__(self, db: Session):
        self._db = db

    def get_proxies(self, limit: int, offset: int) -> list[Proxy]:
        return self._db.query(Proxy).offset(offset).limit(limit).all()

    def get_proxy(self, proxy_id: int) -> Proxy | None:
        return self._db.get(Proxy, (proxy_id,))

    @logger.catch(BaseException)
    def create_proxies(self, proxies: set[ProxyCreate]) -> list[Proxy]:
        instances = [proxy.model_dump() for proxy in proxies]
        instances = self._db.scalars(insert(Proxy).on_conflict_do_nothing().returning(Proxy), instances)
        self._db.commit()
        return instances

    def delete_proxy(self, proxy_id: int) -> None:
        proxy_instance = self.get_proxy(proxy_id)
        if proxy_instance:
            self._db.delete(proxy_instance)
            self._db.commit()

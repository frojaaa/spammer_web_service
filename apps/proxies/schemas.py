from typing import Literal

from pydantic import BaseModel

from apps.dependencies import ProxyProtocol


class ProxyBase(BaseModel):
    protocol: ProxyProtocol
    host: str
    username: str
    password: str

    def __hash__(self):
        return hash(f"{'_'.join((self.protocol, self.host, self.username, self.password))}")


class Proxy(ProxyBase):
    class Config:
        orm_mode = True


class ProxyCreate(ProxyBase):
    pass

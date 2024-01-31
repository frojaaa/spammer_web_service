from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from apps.dependencies import ProxyProtocol
from db import Base


class Proxy(Base):
    __tablename__ = 'proxies'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    protocol: Mapped[ProxyProtocol] = mapped_column(
        Enum("http", "socks4", "socks5", name="proxy_protocol"),
    )
    host: Mapped[str]
    username: Mapped[str]
    password: Mapped[str]

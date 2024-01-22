from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from apps.dependencies import ProxyProtocol
from db import Base


class Proxy(Base):
    __tablename__ = 'proxies'

    protocol: Mapped[ProxyProtocol] = mapped_column(
        Enum("http", "socks4", "socks5", name="proxy_protocol"), primary_key=True,
    )
    host: Mapped[str] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(primary_key=True)
    password: Mapped[str] = mapped_column(primary_key=True)

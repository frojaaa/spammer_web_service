from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship


from db import Base
from ..chats.models import Chat
from ..subscriptions.models import Subscription


class Account(Base):
    __tablename__ = 'accounts'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    api_hash: Mapped[str]
    name: Mapped[str] = mapped_column(unique=True)
    message: Mapped[str]
    chats: Mapped[list[Chat]] = relationship(Chat)
    subscriptions: Mapped[list[Subscription]] = relationship(Subscription)

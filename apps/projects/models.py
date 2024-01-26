from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship

from db import Base
from ..accounts.models import Account
from ..chats.models import Chat
from ..subscriptions.models import Subscription


class Project(Base):
    __tablename__ = 'projects'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    message: Mapped[str]
    accounts: Mapped[list[Account]] = relationship(Account)
    chats: Mapped[list[Chat]] = relationship(Chat)
    subscriptions: Mapped[list[Subscription]] = relationship(Subscription)

from pydantic import BaseModel

from apps.chats.schemas import Chat
from apps.subscriptions.schemas import Subscription


class AccountBase(BaseModel):
    id: int
    name: str
    api_hash: str
    message: str

    def __hash__(self):
        return hash(f"{self.id}_{self.name}")


class Account(AccountBase):
    chats: list[Chat] = []
    subscriptions: list[Subscription] = []

    class Config:
        orm_mode = True


class AccountCreate(AccountBase):
    pass

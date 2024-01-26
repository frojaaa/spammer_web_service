from pydantic import BaseModel

from apps.chats.schemas import Chat
from apps.subscriptions.schemas import Subscription
from apps.accounts.schemas import Account


class ProjectBase(BaseModel):
    id: int
    name: str
    message: str

    def __hash__(self):
        return hash(f"{self.id}_{self.name}")


class Project(ProjectBase):
    accounts: list[Account] = []
    chats: list[Chat] = []
    subscriptions: list[Subscription] = []

    class Config:
        orm_mode = True


class ProjectCreate(ProjectBase):
    pass

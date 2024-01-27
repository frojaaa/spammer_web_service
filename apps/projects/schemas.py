from pydantic import BaseModel

from apps.chats.schemas import Chat
from apps.subscriptions.schemas import Subscription
from apps.accounts.schemas import Account


class ProjectBase(BaseModel):
    name: str
    message: str

    def __hash__(self):
        return hash(f"{self.name}_{self.message}")


class Project(ProjectBase):
    id: int
    accounts: list[Account] = []
    chats: list[Chat] = []
    subscriptions: list[Subscription] = []

    class Config:
        orm_mode = True


class ProjectCreate(ProjectBase):
    pass


class ProjectEdit(ProjectBase):
    id: int

from pydantic import BaseModel


class SubscriptionBase(BaseModel):
    chat_id: str
    project_id: int

    def __hash__(self):
        return hash(f"{self.chat_id}_{self.project_id}")


class Subscription(SubscriptionBase):
    class Config:
        orm_mode = True


class SubscriptionCreate(SubscriptionBase):
    pass

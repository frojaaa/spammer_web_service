from pydantic import BaseModel


class SubscriptionBase(BaseModel):
    chat_id: str
    account_id: int

    def __hash__(self):
        return hash(f"{self.chat_id}_{self.account_id}")


class Subscription(SubscriptionBase):
    class Config:
        orm_mode = True


class SubscriptionCreate(SubscriptionBase):
    pass

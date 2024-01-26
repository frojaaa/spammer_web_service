from pydantic import BaseModel


class AccountBase(BaseModel):
    id: int
    name: str
    api_hash: str
    project_id: int

    def __hash__(self):
        return hash(f"{self.id}_{self.name}")


class Account(AccountBase):
    class Config:
        orm_mode = True


class AccountCreate(AccountBase):
    pass

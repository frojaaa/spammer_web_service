from pydantic import BaseModel


class AccountBase(BaseModel):
    name: str
    project_id: int

    def __hash__(self):
        return hash(f"{self.project_id}_{self.name}")


class Account(AccountBase):
    id: int

    class Config:
        orm_mode = True


class AccountCreate(AccountBase):
    pass

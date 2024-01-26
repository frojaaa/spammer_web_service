from pydantic import BaseModel


class ChatBase(BaseModel):
    id: str
    project_id: int

    def __hash__(self):
        return hash(f"{self.id}_{self.project_id}")


class Chat(ChatBase):
    class Config:
        orm_mode = True


class ChatCreate(ChatBase):
    pass

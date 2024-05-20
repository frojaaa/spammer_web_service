from loguru import logger
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

from .models import Chat
from .schemas import ChatCreate, ChatBase
from ..dependencies import Singleton


class ChatsService(metaclass=Singleton):
    def __init__(self, db: Session):
        self._db = db

    def get_chat(self, chat: ChatBase) -> Chat | None:
        return self._db.get(Chat, (chat.id, chat.project_id))

    def get_chats(self, limit: int, offset: int) -> list[Chat]:
        return self._db.query(Chat).offset(offset).limit(limit).all()

    def create_chats(self, chats: set[ChatCreate]) -> list[Chat]:
        instances = [chat.model_dump() for chat in chats]
        instances = self._db.scalars(insert(Chat).on_conflict_do_nothing().returning(Chat), instances)
        self._db.commit()
        return instances

    def delete_chat(self, chat: ChatCreate) -> None:
        chat_instance = self.get_chat(chat)
        if chat_instance:
            self._db.delete(chat_instance)
            self._db.commit()
        else:
            raise Exception('chat does not exist')

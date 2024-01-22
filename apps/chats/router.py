from fastapi import APIRouter, Depends, HTTPException, status

from typing import Annotated

from .service import ChatsService
from .schemas import Chat, ChatCreate
from db import SessionLocal
from ..dependencies import common_parameters
from ..schemas import CommonParams

router = APIRouter(prefix='/chats', tags=['chats'], responses={404: {"description": "Not found"}})
CommonsDep = Annotated[CommonParams, Depends(common_parameters)]


def get_chats_service() -> ChatsService:
    db = SessionLocal()
    service = ChatsService(db)
    try:
        yield service
    finally:
        db.close()


@router.get('/', response_model=list[Chat])
def read_chats(
        commons: CommonsDep,
        service: ChatsService = Depends(get_chats_service)
) -> list[Chat]:
    chats = service.get_chats(commons.limit, commons.offset)
    return chats


@router.post('/get_chat', response_model=Chat)
def read_chat(chat: Chat, service: ChatsService = Depends(get_chats_service)):
    chat = service.get_chat(chat)
    if not chat:
        raise HTTPException(status_code=404, detail="chat not found")
    return chat


@router.delete('/delete', status_code=status.HTTP_204_NO_CONTENT)
def delete_chat(chat: ChatCreate, service: ChatsService = Depends(get_chats_service)):
    service.delete_chat(chat)


@router.post('/create', response_model=list[ChatCreate], status_code=status.HTTP_201_CREATED)
def create_chats(chats: set[ChatCreate], service: ChatsService = Depends(get_chats_service)):
    return service.create_chats(chats)

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile

from typing import Annotated

from settings import BASE_DIR
from .service import AccountsService
from .schemas import Account, AccountCreate
from db import SessionLocal
from ..dependencies import common_parameters
from ..schemas import CommonParams

router = APIRouter(prefix='/accounts', tags=['accounts'], responses={404: {"description": "Not found"}})
CommonsDep = Annotated[CommonParams, Depends(common_parameters)]


def get_accounts_service() -> AccountsService:
    db = SessionLocal()
    service = AccountsService(db)
    try:
        yield service
    finally:
        db.close()


@router.get('/', response_model=list[Account])
def read_accounts(
        commons: CommonsDep,
        service: AccountsService = Depends(get_accounts_service)
) -> list[Account]:
    accounts = service.get_accounts(commons.limit, commons.offset)
    return accounts


@router.get('/{account_id}', response_model=Account)
def read_account(account_id: int, service: AccountsService = Depends(get_accounts_service)):
    account = service.get_account(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.delete('/{account_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_account(account_id: int, service: AccountsService = Depends(get_accounts_service)):
    service.delete_account(account_id)


@router.post('/create', response_model=list[Account], status_code=status.HTTP_201_CREATED)
def create_accounts(accounts: set[AccountCreate], service: AccountsService = Depends(get_accounts_service)):
    return service.create_accounts(accounts)


@router.post("/sessions/{project_id}", status_code=status.HTTP_201_CREATED)
async def upload_file(project_id: int, files: list[UploadFile]):
    if not files:
        raise HTTPException(status_code=400, detail="No files were sent")
    SESSIONS_DIR = BASE_DIR / 'sessions' / str(project_id)
    SESSIONS_DIR.mkdir(exist_ok=True)
    for file in files:
        file_path = SESSIONS_DIR / file.filename
        with open(file_path, 'wb') as f:
            f.write(await file.read())


@router.delete("/sessions/{project_id}/{account_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(project_id: int, account_name: str):
    SESSIONS_DIR = BASE_DIR / 'sessions' / str(project_id)
    if not SESSIONS_DIR.exists():
        raise HTTPException(status_code=404, detail=f"There are no files associated with {project_id} accounts")
    session_file = SESSIONS_DIR / f"{account_name}.session"
    if not session_file.exists():
        raise HTTPException(status_code=404, detail=f"There are no files associated with {account_name} account")
    session_file.unlink()

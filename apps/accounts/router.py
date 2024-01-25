from fastapi import APIRouter, Depends, HTTPException, status

from typing import Annotated

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


@router.put('/{account_id}', response_model=Account, status_code=status.HTTP_201_CREATED)
def update_account(account_id: int, account: AccountCreate, service: AccountsService = Depends(get_accounts_service)):
    acc = service.get_account(account_id)
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
    acc = service.edit_account(account)
    return acc


@router.post('/create', response_model=list[Account], status_code=status.HTTP_201_CREATED)
def create_accounts(accounts: set[AccountCreate], service: AccountsService = Depends(get_accounts_service)):
    return service.create_accounts(accounts)

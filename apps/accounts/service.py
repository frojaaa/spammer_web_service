from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from .models import Account
from .schemas import AccountCreate


class AccountsService:
    def __init__(self, db: Session):
        self._db = db

    def get_account(self, id_: int) -> Account | None:
        return self._db.get(Account, (id_,))

    def get_accounts(self, limit: int, offset: int) -> list[Account]:
        return self._db.query(Account).offset(offset).limit(limit).all()

    def create_accounts(self, accounts: set[AccountCreate]) -> list[Account]:
        instances = [account.model_dump() for account in accounts]
        instances = self._db.scalars(insert(Account).on_conflict_do_nothing().returning(Account), instances)
        self._db.commit()
        return instances

    def delete_account(self, id_: int) -> None:
        self._db.query(Account).filter(Account.id == id_).delete()
        self._db.commit()

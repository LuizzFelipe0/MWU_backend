from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session
from mwu.repositories.base_repository import BaseRepository
from .models import Transactions as TransactionModel

class TransactionsRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session=session, model=TransactionModel)

    def _get_transaction_scoped_query(self, user_id: UUID, is_deleted: bool = False):
        return self._get_query().filter(
            self.model.user_id == user_id,
            self.model.deleted_at.isnot(None) if is_deleted else self.model.deleted_at.is_(None)
        )

    def get_transactions_by_user(self, user_id: UUID):
        return self._get_transaction_scoped_query(user_id).all()

    def get_deleted_transactions_by_user(self, user_id: UUID):
        return self._get_transaction_scoped_query(user_id, is_deleted=True).all()

    def get_transaction_by_user(self, transaction_id: UUID, user_id: UUID):
        transaction = self._get_transaction_scoped_query(user_id).filter(self.model.id == transaction_id).first()

        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return transaction
    
    def get_deleted_transaction_by_user(self, transaction_id: UUID, user_id: UUID):
        transaction = self._get_transaction_scoped_query(user_id, is_deleted=True).filter(
            self.model.id == transaction_id).first()
        if not transaction:
            raise HTTPException(status_code=404, detail="Deleted transaction not found")
        return transaction
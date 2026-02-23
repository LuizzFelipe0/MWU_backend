from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from auth.utils import get_current_user
from .schemas import TransactionOutput as TransactionOutScheme, TransactionInput, TransactionUpdateInput
from .service import TransactionsService

transactions_router = APIRouter(prefix="/transactions", tags=["Transactions"])


@cbv(transactions_router)
class TransactionsController:
    service: TransactionsService = Depends()

    @transactions_router.get("/all", response_model=list[TransactionOutScheme | None])
    def get_all_transactions(self, current_user = Depends(get_current_user)):
        transactions = self.service.get_all_transactions(user_id=current_user.id)
        return transactions

    @transactions_router.get("/deleted", response_model=list[TransactionOutScheme | None])
    def get_deleted_transactions(self, current_user = Depends(get_current_user)):
        deleted_transactions = self.service.get_deleted_transactions(user_id=current_user.id)
        return deleted_transactions

    @transactions_router.get("/{transaction_id}", response_model=TransactionOutScheme | None)
    def get_transaction_by_id(self, transaction_id: UUID, current_user = Depends(get_current_user)):
        transaction = self.service.get_transaction_by_id(id=transaction_id, user_id=current_user.id)
        return transaction

    @transactions_router.post("/create", response_model=TransactionOutScheme, status_code=201)
    def create_transaction(self, data: TransactionInput, current_user = Depends(get_current_user)) -> TransactionOutScheme:
        transaction = self.service.create_transaction(data, user_id=current_user.id)
        return transaction

    @transactions_router.patch("/{transaction_id}/update", status_code=200)
    def update_transaction(self, transaction_id: UUID, data: TransactionUpdateInput, current_user = Depends(get_current_user)) -> TransactionOutScheme:
        transaction = self.service.update_transaction(id=transaction_id, data=data, user_id=current_user.id)
        return transaction

    @transactions_router.delete("/{transaction_id}/delete", status_code=200)
    def delete_transaction(self, transaction_id: UUID, current_user = Depends(get_current_user)) -> TransactionOutScheme:
        transaction = self.service.delete_transaction(id=transaction_id, user_id=current_user.id)
        return transaction

    @transactions_router.post("/{transaction_id}/restore", status_code=200)
    def restore_transaction(self, transaction_id: UUID, current_user = Depends(get_current_user)) -> TransactionOutScheme:
        transaction = self.service.restore_transaction(id=transaction_id, user_id=current_user.id)
        return transaction

    @transactions_router.delete("/{transaction_id}/force-delete", status_code=204)
    def force_delete_transaction(self, transaction_id: UUID, current_user = Depends(get_current_user)):
        transaction = self.service.force_delete_transaction(id=transaction_id, user_id=current_user.id)
        return transaction

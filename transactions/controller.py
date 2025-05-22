from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from .service import TransactionsService
from .schemas import TransactionOutput as TransactionOutScheme, TransactionInput, TransactionUpdateInput

transactions_router = APIRouter(prefix="/transactions", tags=["Transactions"])


@cbv(transactions_router)
class TransactionsController:
    service: TransactionsService = Depends()

    @transactions_router.get("/all", response_model=list[TransactionOutScheme | None])
    def get_all_transactions(self):
        transactions = self.service.get_all_transactions()
        return transactions

    @transactions_router.get("/deleted", response_model=list[TransactionOutScheme | None])
    def get_deleted_transactions(self):
        deleted_transactions = self.service.get_deleted_transactions()
        return deleted_transactions

    @transactions_router.get("/{transaction_id}", response_model=TransactionOutScheme | None)
    def get_transaction_by_id(self, transaction_id: UUID):
        transaction = self.service.get_transaction_by_id(id=transaction_id)
        return transaction
    
    @transactions_router.post("/create", response_model=TransactionOutScheme, status_code=201)
    def create_transaction(self, data: TransactionInput) -> TransactionOutScheme:
        transaction = self.service.create_transaction(data)
        return transaction

    @transactions_router.patch("/{transaction_id}/update", status_code=200)
    def update_transaction(self, transaction_id: UUID, data: TransactionUpdateInput) -> TransactionOutScheme:
        transaction = self.service.update_transaction(id=transaction_id, data=data)
        return transaction

    @transactions_router.delete("/{transaction_id}/delete", status_code=200)
    def delete_transaction(self, transaction_id: UUID) -> TransactionOutScheme:
        transaction = self.service.delete_transaction(id=transaction_id)
        return transaction

    @transactions_router.post("{transaction_id}/restore", status_code=200)
    def restore_transaction(self, transaction_id: UUID) -> TransactionOutScheme:
        transaction = self.service.restore_transaction(id=transaction_id)
        return transaction
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from mwu.repositories.base_repository import BaseRepository
from .models import UsersAccounts as UsersAccountsModel


class UserAccountsRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session=session, model=UsersAccountsModel)

    def get_relation(self, user_id: UUID, account_id: UUID):
        return self._get_query().filter_by(
            user_id=user_id,
            account_id=account_id
        ).first()

    def get_relation_by_user(self, user_id: UUID):
        return self._get_query().filter_by(user_id=user_id).all()

    def get_relation_by_account(self, account_id: UUID):
        return self._get_query().filter_by(account_id=account_id).all()

    def create_relation(self, user_id: UUID, account_id: UUID):
        if self.get_relation(user_id, account_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This user is already registered to this account."
            )

        obj = self.model(user_id=user_id, account_id=account_id)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete_relation(self, user_id: UUID, account_id: UUID):
        relation = self.get_relation(user_id, account_id)
        if not relation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User account not found."
            )

        self.db.delete(relation)
        self.db.commit()
        return
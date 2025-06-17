from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from accounts.models import Accounts as AccountModel
from mwu.db import get_db
from mwu.repositories.operational_repositories import ModelRelationRepository, ModelOperationalRepository
from user.models import User as UserModel
from .models import UsersAccounts as UserAccountModel


class UserAccountService:
    def __init__(self, session: Session = Depends(get_db)):
        self.db = session
        self.relation_repository = ModelRelationRepository(
            relation_model=UserAccountModel,
            first_model_key="user_id",
            second_model_key="account_id",
            session=session
        )
        self.user_repository = ModelOperationalRepository(UserModel, session=session)
        self.account_repository = ModelOperationalRepository(AccountModel, session=session)

    def get_all_user_accounts(self):
        user_accounts = self.relation_repository.get_all_relations()
        return user_accounts

    def create_user_account_relation(self, user_id: UUID, account_id: UUID):
        self.user_repository.get_obj_by_id_not_deleted(user_id)
        self.account_repository.get_obj_by_id_not_deleted(account_id)

        create_user_account_relation = self.relation_repository.create_relationship(user_id, account_id)
        return create_user_account_relation

    def delete_user_account_relation(self, user_id: UUID, account_id: UUID):
        delete_user_account_relation = self.relation_repository.delete_relationship(user_id, account_id)

        return delete_user_account_relation

    def get_accounts_for_user_relation(self, user_id: UUID):
        accounts_for_users = self.relation_repository.get_relations_by_key("user_id", user_id)

        return accounts_for_users

    def get_users_for_account_relation(self, account_id: UUID):
        users_for_account = self.relation_repository.get_relations_by_key("account_id", account_id)

        return users_for_account

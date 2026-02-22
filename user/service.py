from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from auth.security import is_strong_password, hash_password
from mwu.db import get_db

from .repository import UserRepository
from .schemas import UserInput as UserInScheme, UserUpdateInput as UserUpdateInScheme
from .utils import cpf_validator


class UserService:
    def __init__(self, session: Session = Depends(get_db)):
        self.user_repository = UserRepository(session)

    def get_all_users(self):
        users = self.user_repository.get_all()
        return users

    def get_deleted_users(self):
        users = self.user_repository.get_all_deleted_users()
        return users

    def get_user_by_id(self, id: UUID):
        user = self.user_repository.get_by_id(obj_id=id)
        return user

    def create_user(self, data: UserInScheme):
        is_strong_password(data.password)
        cpf_validator(data.cpf)

        hashed_password = hash_password(data.password)

        user_data = data.dict()
        user_data['password'] = hashed_password
        user_data['cpf'] = cpf_validator(user_data['cpf'])
        user_data['is_admin'] = False

        user = self.user_repository.create(data=UserInScheme(**user_data))

        return user

    def update_user(self, id: UUID, data: UserUpdateInScheme):
        user_with_id_validated = self.user_repository.get_by_id(id)

        user_data = data.dict(exclude_unset=True)

        if 'password' in user_data:
            is_strong_password(user_data['password'])
            user_data['password'] = hash_password(user_data['password'])

        if 'cpf' in user_data:
            user_data['cpf'] = cpf_validator(user_data['cpf'])

        user = self.user_repository.update(obj_id=user_with_id_validated.id, data=UserUpdateInScheme(**user_data))

        return user

    def delete_user(self, id: UUID):
        user_with_id_validated = self.user_repository.get_by_id(id)
        user = self.user_repository.soft_delete(obj_id=user_with_id_validated.id)
        return user

    def restore_user(self, id: UUID):
        user_with_id_validated = self.user_repository.get_by_id(id)
        user = self.user_repository.restore(obj_id=user_with_id_validated.id)
        return user

    def force_delete_user(self, id: UUID):
        user_with_id_validated = self.user_repository.get_by_id(id)
        user = self.user_repository.force_delete(obj_id=user_with_id_validated.id)
        return user

from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from mwu.db import get_db
from mwu.services import ModelOperationalService
from .auth.security import is_strong_password, hash_password
from .models import User as UserModel
from .schemas import UserInput as UserInScheme, UserUpdateInput as UserUpdateInScheme
from .utils import cpf_validator


class UserRepository(ModelOperationalService):
    def __init__(self, session: Session = Depends(get_db)):
        super().__init__(model=UserModel, session=session)

    def get_all_users(self):
        users = self.get_all_not_deleted()
        return users

    def get_deleted_users(self):
        users = self.get_all_deleted()
        return users

    def get_user_by_id(self, id: UUID):
        user = self.get_obj_by_id_not_deleted(obj_id=id)
        return user

    def create_user(self, data: UserInScheme):
        is_strong_password(data.password)
        cpf_validator(data.cpf)

        hashed_password = hash_password(data.password)
        user_data = data.dict()
        user_data['password'] = hashed_password
        user_data['cpf'] = cpf_validator(user_data['cpf'])

        user = self.create(data=UserInScheme(**user_data))
        return user

    def update_user(self, id: UUID, data: UserUpdateInScheme):
        user_with_id_validated = self.get_obj_by_id_not_deleted(id)

        if data.password is not None:
            is_strong_password(data.password)

        if data.cpf is not None:
            cpf_validator(data.cpf)

        user = self.update(obj_id=user_with_id_validated.id, data=data)
        return user

    def delete_user(self, id: UUID):
        user_with_id_validated = self.get_obj_by_id_not_deleted(id)
        user = self.delete(obj_id=user_with_id_validated.id)
        return user

    def restore_user(self, id: UUID):
        user_with_id_validated = self.get_obj_by_id_deleted(id)
        user = self.restore(obj_id=user_with_id_validated.id)
        return user

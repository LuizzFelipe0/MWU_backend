from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from category_types.repository import CategoryTypeRepository
from mwu.db import get_db

from .repository import CategoryRepository
from .schemas import CategoryInput as CategoryInScheme, CategoryUpdateInput as CategoryUpdateInScheme


class CategoryService:
    def __init__(self, session: Session = Depends(get_db)):
        self.category_repository = CategoryRepository(session=session)
        self.category_type_repository = CategoryTypeRepository

    def get_all_categories(self, user_id: UUID):
        categories = self.category_repository.get_categories_by_user(user_id=user_id)
        return categories

    def get_deleted_categories(self, user_id: UUID):
        deleted_categories = self.category_repository.get_deleted_categories_by_user(user_id=user_id)
        return deleted_categories

    def get_category_by_id(self, id: UUID, user_id: UUID):
        category = self.category_repository.get_category_by_user(category_id=id, user_id=user_id)

        return category

    def create_category(self, data: CategoryInScheme, user_id: UUID):
        data.user_id = user_id

        category = self.category_repository.create(data=data)
        return category

    def update_category(self, id: UUID, data: CategoryUpdateInScheme,user_id: UUID):
        self.category_repository.get_category_by_user(category_id=id, user_id=user_id)

        if data.category_type_id:
            self.category_type_repository.get_by_id(data.category_type_id)

        data.user_id = user_id

        category = self.category_repository.update(obj_id=id, data=data)
        return category

    def delete_category(self, id: UUID, user_id: UUID):
        category_validated = self.category_repository.get_category_by_user(category_id=id, user_id=user_id)

        category = self.category_repository.soft_delete(obj_id=category_validated.id)
        return category

    def restore_category(self, id: UUID, user_id: UUID):
        deleted_category_validated = self.category_repository.get_deleted_category_by_user(category_id=id, user_id=user_id)

        category = self.category_repository.restore(obj_id=deleted_category_validated.id)
        return category

    def force_delete_category(self, id: UUID, user_id: UUID):
        deleted_category_validated = self.category_repository.get_deleted_category_by_user(category_id=id, user_id=user_id)

        category = self.category_repository.force_delete(obj_id=deleted_category_validated.id)
        return category

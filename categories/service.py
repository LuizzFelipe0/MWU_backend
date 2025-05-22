from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from category_types.models import CategoryTypes as CategoryTypeModel
from mwu.db import get_db
from mwu.repositories.operational_repositories import ModelOperationalRepository
from user.models import User as UserModel
from .models import Category as CategoryModel
from .schemas import CategoryInput as CategoryInScheme, CategoryUpdateInput as CategoryUpdateInScheme


class CategoryService(ModelOperationalRepository):
    def __init__(self, session: Session = Depends(get_db)):
        super().__init__(model=CategoryModel, session=session)
        self.user_service = ModelOperationalRepository(UserModel, session=session)
        self.category_type_service = ModelOperationalRepository(CategoryTypeModel, session=session)

    def get_all_categories(self):
        categories = self.get_all()
        return categories

    def get_deleted_categories(self):
        deleted_categories = self.get_all_deleted()
        return deleted_categories

    def get_category_by_id(self, id: UUID):
        category = self.get_obj_by_id_not_deleted(obj_id=id)
        return category

    def create_category(self, data: CategoryInScheme):
        self.user_service.get_obj_by_id_not_deleted(data.user_id)
        self.category_type_service.get_obj_by_id(data.category_type_id)

        category = self.create(data=data)
        return category

    def update_category(self, id: UUID, data: CategoryUpdateInScheme):  # Need improvement
        category_with_id_validated = self.get_obj_by_id(id)

        if data.user_id is not None:
            self.get_obj_by_id_not_deleted(data.user_id)
        elif data.category_type_id is not None:
            self.get_obj_by_id(data.category_type_id)

        category = self.update(obj_id=category_with_id_validated.id, data=data)
        return category

    def delete_category(self, id: UUID):
        category_with_id_validated = self.get_obj_by_id(id)
        category = self.delete(obj_id=category_with_id_validated.id)
        return category

    def restore_category(self, id: UUID):
        category_with_id_validated = self.get_obj_by_id_deleted(id)
        category = self.restore(obj_id=category_with_id_validated.id)
        return category

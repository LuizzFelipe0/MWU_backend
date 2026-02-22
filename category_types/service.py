from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from mwu.db import get_db
from .repository import CategoryTypeRepository
from .schemas import CategoryTypesInput as CategoryTypeInScheme, CategoryTypesUpdateInput as CategoryTypesUpdateInScheme


class CategoryTypeService:
    def __init__(self, session: Session = Depends(get_db)):
        self.category_type_repository = CategoryTypeRepository(session)

    def get_all_category_types(self):
        category_types = self.category_type_repository.get_all()
        return category_types

    def get_category_type_by_id(self, category_type_id: UUID):
        category_type = self.category_type_repository.get_by_id(obj_id=category_type_id)
        return category_type

    def create_category_type(self, data: CategoryTypeInScheme):
        category_type = self.category_type_repository.create(data=data)
        return category_type

    def update_category_type(self, id: UUID, data: CategoryTypesUpdateInScheme):
        category_type_with_id_validated = self.category_type_repository.get_by_id(id)
        category_type = self.category_type_repository.update(obj_id=category_type_with_id_validated.id, data=data)
        return category_type

    def delete_category_type(self, id: UUID):
        category_type = self.category_type_repository.force_delete(obj_id=id)
        return category_type
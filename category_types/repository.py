from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from category_types.models import CategoryTypes as CategoryTypesModel
from mwu.db import get_db
from mwu.services import ModelOperationalService
from .schemas import CategoryTypesInput as CategoryTypeInScheme, CategoryTypesUpdateInput as CategoryTypesUpdateInScheme


class CategoryTypeRepository(ModelOperationalService):
    def __init__(self, session: Session = Depends(get_db)):
        super().__init__(model=CategoryTypesModel, session=session)

    def get_all_category_types(self):
        category_types = self.get_all()
        return category_types

    def create_category_type(self, data: CategoryTypeInScheme):  # Need to guarantee data is a Pydantic object
        category_type = self.create(data=data)
        return category_type

    def update_category_type(self, id: UUID, data: CategoryTypesUpdateInScheme):
        category_type_with_id_validated = self.get_obj_by_id(id)
        category_type = self.update(obj_id=category_type_with_id_validated.id, data=data)
        return category_type

    def delete_category_type(self, id: UUID):
        category_type = self.force_delete(obj_id=id)
        return category_type
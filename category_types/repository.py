from fastapi import Depends
from sqlalchemy.orm import Session

from category_types.models import CategoryTypes as CategoryTypesModel
from mwu.db import get_db
from mwu.services import ModelOperationalService


class CategoryTypeRepository(ModelOperationalService):
    def __init__(self, session: Session = Depends(get_db)):
        super().__init__(model=CategoryTypesModel, session=session)

    def get_all_category_types(self):
        category_types = self.get_all()
        return category_types

    def create_category_type(self, data):
        category_type = self.create(data=data)
        return category_type

    def update_category_type(self, id, data):
        id_validated = self.get_obj_by_id(id)
        category_type = self.update(id=id_validated, data=data)
        return category_type

    def delete_category_type(self, id):
        category_type = self.force_delete(id=id)
        return category_type

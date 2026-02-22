from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from mwu.repositories.base_repository import BaseRepository
from .models import Category as CategoryModel

class CategoryRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session=session, model=CategoryModel)

    def _get_category_scoped_query(self, user_id: UUID, is_deleted: bool = False):
        return self._get_query().filter(
            self.model.user_id == user_id,
            self.model.deleted_at.isnot(None) if is_deleted else self.model.deleted_at.is_(None)
        )

    def get_categories_by_user(self, user_id: UUID):
        return self._get_category_scoped_query(user_id).all()

    def get_deleted_categories_by_user(self, user_id: UUID):
        return self._get_category_scoped_query(user_id, is_deleted=True).all()

    def get_category_by_user(self, category_id: UUID, user_id: UUID):
        category = self._get_category_scoped_query(user_id).filter(self.model.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category

    def get_deleted_category_by_user(self, category_id: UUID, user_id: UUID):
        category = self._get_category_scoped_query(user_id, is_deleted=True).filter(self.model.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Deleted category not found")
        return category
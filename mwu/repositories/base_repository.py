from datetime import datetime
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

class BaseRepository:
    def __init__(self, session: Session, model):
        self.db = session
        self.model = model

    def _get_query(self):
        return self.db.query(self.model)

    def get_all(self):
        return self._get_query().all()

    def get_by_id(self, obj_id: UUID, must_exist: bool = True):
        obj = self._get_query().filter(self.model.id == obj_id).first()

        if not obj and must_exist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__name__} not found"
            )
        return obj

    def create(self, data: BaseModel):
        obj = self.model(**data.dict())

        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, obj_id: UUID, data: BaseModel):
        obj = self.get_by_id(obj_id)

        for key, val in data.dict(exclude_unset=True).items():
            setattr(obj, key, val)

        if hasattr(obj, "updated_at"):
            obj.updated_at = datetime.now()

        self.db.commit()
        self.db.refresh(obj)

        return obj

    def soft_delete(self, obj_id: UUID):
        obj = self.get_by_id(obj_id)

        if hasattr(obj, "deleted_at"):
            obj.deleted_at = datetime.now()
            self.db.commit()
            self.db.refresh(obj)
        return obj

    def restore(self, obj_id: UUID):
        obj = self.get_by_id(obj_id)

        if hasattr(obj, "deleted_at"):
            obj.deleted_at = None
            self.db.commit()
            self.db.refresh(obj)
        return obj

    def force_delete(self, obj_id: UUID):
        obj = self.get_by_id(obj_id)

        self.db.delete(obj)
        self.db.commit()
        return True
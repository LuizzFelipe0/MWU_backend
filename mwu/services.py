from datetime import datetime
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from .db import get_db


class BaseService:
    def __init__(self, session: Session = Depends(get_db)):
        self.db = session


class ModelOperationalService(BaseService):
    def __init__(self, model, session: Session = Depends(get_db)):
        super().__init__(session)
        self.model = model

    def get_all(self):
        return self.db.query(self.model).all()

    def get_all_not_deleted(self):
        return self.db.query(self.model).filter(self.model.deleted_at.is_(None)).all()

    def get_all_deleted(self):
        return self.db.query(self.model).filter(self.model.deleted_at.isnot(None)).all()

    def get_obj_by_id(self, obj_id: UUID):
        obj = self.db.query(self.model).filter(self.model.id == obj_id).first()
        if not obj:
            raise HTTPException(status_code=404, detail={self.model.__name__: "Not found"})
        return obj

    def get_obj_by_id_not_deleted(self, obj_id: UUID):
        obj = self.db.query(self.model).filter(self.model.id == obj_id, self.model.deleted_at.is_(None)).first()
        if not obj:
            raise HTTPException(status_code=404, detail={self.model.__name__: "Not found"})
        return obj

    def get_obj_by_id_deleted(self, obj_id: UUID):
        obj = self.db.query(self.model).filter(self.model.id == obj_id, self.model.deleted_at.isnot(None)).first()
        if not obj:
            raise HTTPException(status_code=404,
                                detail={self.model.__name__: "Not found, Object may be deleted or does not exist"})
        return obj

    def create(self, data):
        obj = self.model(**data.dict())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, obj_id: UUID, data):
        obj = self.db.query(self.model).filter(self.model.id == obj_id).first()
        for key, val in data.dict(exclude_unset=True).items():
            setattr(obj, key, val)
        obj.updated_at = datetime.now()
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj_id: UUID):
        obj = self.get_obj_by_id_not_deleted(obj_id)
        obj.deleted_at = datetime.now()
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def restore(self, obj_id: UUID):
        deleted_obj = self.get_obj_by_id_deleted(obj_id)
        deleted_obj.updated_at = datetime.now()
        deleted_obj.deleted_at = None
        self.db.commit()
        self.db.refresh(deleted_obj)
        return deleted_obj

    def force_delete(self, obj_id: UUID):
        obj = self.db.query(self.model).filter(self.model.id == obj_id).first()
        self.db.delete(obj)
        self.db.commit()
        raise HTTPException(status_code=204)


"""class ModelRelationService(BaseService):
    def __init__(self, model, session: Session = Depends(get_db)):
        super().__init__(session)
        self.model = model

    def create_relationship(self, first_obj_id: UUID, second_obj_id:UUID):
        first_obj = ModelOperationalService.get_obj_by_id_not_deleted(first_obj_id)
        second_obj = ModelOperationalService.get_obj_by_id_not_deleted(second_obj_id)
        relationship = 
"""

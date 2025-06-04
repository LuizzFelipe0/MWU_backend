from datetime import datetime
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from mwu.db import get_db


class BaseRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.db = session


class ModelOperationalRepository(BaseRepository):
    def __init__(self, model, session: Session = Depends(get_db)):
        super().__init__(session)
        self.model = model

    def get_all(self):
        return self.db.query(self.model).all()

    def get_all_not_deleted(self):
        return self.db.query(self.model).filter(self.model.deleted_at.is_(None)).all()

    def get_all_deleted(self):
        return self.db.query(self.model).filter(self.model.deleted_at.isnot(None)).all()

    def get_objs_by_key(self, key: str, key_value: UUID, has_deleted_at: bool = True):
        if not hasattr(self.model, key):
            raise HTTPException(
                status_code=400, detail=f"Key '{key}' not found in model {self.model.__name__}"
            )
        query = self.db.query(self.model).filter(getattr(self.model, key) == key_value)

        if has_deleted_at:
            if not hasattr(self.model, "deleted_at"):
                raise HTTPException(
                    status_code=500,
                    detail=f"Model '{self.model.__name__}' does not have 'deleted_at' field, but 'has_deleted_at=True' was passed.",
                )
            query = query.filter(self.model.deleted_at.is_(None))

        return query.all()

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


class ModelRelationRepository:
    def __init__(
            self,
            relation_model,
            first_model_key: str,
            second_model_key: str,
            session: Session = Depends(get_db)
    ):
        self.db = session
        self.relation_model = relation_model
        self.first_key = first_model_key
        self.second_key = second_model_key

    def get_relations_by_key(self, key: str, value: UUID):
        if key not in [self.first_key, self.second_key]:
            raise HTTPException(status_code=400, detail="Invalid key for relation filter")

        return self.db.query(self.relation_model).filter_by(**{key: value}).all()

    def check_existing_relationship(self, first_id: UUID, second_id: UUID):
        existing_relationship = self.db.query(self.relation_model).filter_by(
            **{self.first_key: first_id, self.second_key: second_id}
        ).first()

        return existing_relationship

    def create_relationship(self, first_id: UUID, second_id: UUID):
        existing_relationship = self.check_existing_relationship(first_id, second_id)

        if existing_relationship:
            raise HTTPException(status_code=404, detail="Relationship already exists")

        relation_obj = self.relation_model(**{
            self.first_key: first_id,
            self.second_key: second_id
        })

        self.db.add(relation_obj)
        self.db.commit()
        self.db.refresh(relation_obj)

        return relation_obj

    def delete_relationship(self, first_id: UUID, second_id: UUID):
        existing_relationship = self.check_existing_relationship(first_id, second_id)

        if not existing_relationship:
            raise HTTPException(status_code=404, detail="Relationship does not exist")

        self.db.delete(existing_relationship)
        self.db.commit()

        return []

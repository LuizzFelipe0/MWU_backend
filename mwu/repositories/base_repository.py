from datetime import datetime
from uuid import UUID
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from mwu.db import get_db


class ModelRelationRepository:
    def init(
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

    def get_all_relations(self):
        relations = self.db.query(self.relation_model).all()
        return relations

    def get_relation_by_id(self, relation_id: UUID):
        relation = self.db.query(self.relation_model).filter(self.relation_model.id == relation_id).first()
        if not relation:
            raise HTTPException(status_code=404, detail={self.relation_model.__name__: "Not found"})
        return relation

    def get_relations_by_key(self, key: str, value: UUID):
        if key not in [self.first_key, self.second_key]:
            raise HTTPException(status_code=400, detail="Invalid key for relation filter")
        relations_by_key = self.db.query(self.relation_model).filter_by(**{key: value}).all()
        return relations_by_key

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
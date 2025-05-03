from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from mwu.db import get_db
from .models import CategoryTypes as CategoryTypesModel
from .schemas import CategoryTypesOutput as CategoryTypesOutScheme, CategoryTypesInput as CategoryTypesInScheme, \
    CategoryTypesUpdateInput as CategoryTypesUpdateInScheme

category_types_router = APIRouter(prefix="/catgeory_types", tags=["Category Types"])


@category_types_router.get("", response_model=list[CategoryTypesOutScheme])
def get_all_category_types(db: Session = Depends(get_db)):
    category_types = db.query(CategoryTypesModel).all()
    return category_types


@category_types_router.post("", response_model=CategoryTypesOutScheme,
                            status_code=201)
def create_category_type(data: CategoryTypesInScheme, db: Session = Depends(get_db)):
    category_type = CategoryTypesModel(
        name=data.name,
        is_positive=data.is_positive)

    db.add(category_type)
    db.commit()
    db.refresh(category_type)

    return category_type


@category_types_router.patch("/update", status_code=200)
def update_category_type(category_type_id: UUID, data: CategoryTypesUpdateInScheme,
                         db: Session = Depends(get_db)) -> CategoryTypesUpdateInScheme:
    category_type = db.query(CategoryTypesModel).filter_by(id=category_type_id).first()

    if not category_type:
        raise HTTPException(status_code=404, detail="Category Type not found")

    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(category_type, key, value)

    db.commit()

    return category_type


@category_types_router.delete("/delete", status_code=204)
def delete_category_type(category_type_id: UUID, db: Session = Depends(get_db)):
    category_type = db.query(CategoryTypesModel).filter_by(id=category_type_id).first()

    if not category_type:
        raise HTTPException(status_code=404, detail="Category Type not found")

    db.delete(category_type)
    db.commit()

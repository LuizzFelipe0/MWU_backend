from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from mwu.db import get_db
from .models import Category as CategoryModel
from .schemas import CategoryOutput as CategoryOutScheme, CategoryInput as CategoryInScheme

categories_router = APIRouter(prefix="/categories", tags=["Category"])


@categories_router.get("")
def get_all_categories(db: Session = Depends(get_db)) -> list[CategoryOutScheme | None]:
    categories = db.query(CategoryModel).all()
    return categories


@categories_router.get("/{category_id}")
def get_category_by_id(category_id: UUID, db: Session = Depends(get_db)) -> list[CategoryOutScheme | None]:
    category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if category is None:
        return HTTPException(status_code=404, detail="Category not found with the given id.")
    return category

"""""
@categories_router.post("", status_code=201, response_model=CategoryOutScheme)
def create_category(data: CategoryInScheme, db: Session = Depends(get_db)) -> CategoryOutScheme:
    category = CategoryModel(
        name=data.name,
        description=data.description
    )
    db.add(category)
    db.commit()
    db.refresh(category)

    return category
"""
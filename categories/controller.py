from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from mwu.db import get_db
from user.models import User as UserModel
from .models import Category as CategoryModel
from .schemas import CategoryOutput as CategoryOutScheme, CategoryInput as CategoryInScheme, \
    CategoryUpdateInput as CategoryUpdateInScheme

categories_router = APIRouter(prefix="/categories", tags=["Category"])


@categories_router.get("")
def get_all_categories(db: Session = Depends(get_db)) -> list[CategoryOutScheme | None]:
    categories = db.query(CategoryModel).filter(CategoryModel.deleted_at.is_(None)).all()
    return categories


@categories_router.get("/deleted")
def get_deleted_categories(db: Session = Depends(get_db)) -> list[CategoryOutScheme | None]:
    deleted_categories = db.query(CategoryModel).filter(CategoryModel.deleted_at.isnot(None)).all()
    return deleted_categories


@categories_router.get("/{category_id}")
def get_category_by_id(category_id: UUID, db: Session = Depends(get_db)) -> list[CategoryOutScheme | None]:
    category = db.query(CategoryModel).filter(CategoryModel.id == category_id,
                                              CategoryModel.deleted_at.is_(None)).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found with the given id.")
    return category


@categories_router.post("", status_code=201, response_model=CategoryOutScheme)
def create_category(data: CategoryInScheme, db: Session = Depends(get_db)) -> CategoryOutScheme:
    user = db.query(UserModel).filter(UserModel.id == data.user_id,
                                      UserModel.deleted_at.is_(None)).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found with the given id.")

    category = CategoryModel(
        user_id=data.user_id,
        name=data.name,
        description=data.description,
        type=data.type
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


@categories_router.post("/{category_id}/restore", status_code=200, response_model=CategoryOutScheme)
def restore_deleted_category(category_id: UUID, db: Session = Depends(get_db)) -> CategoryOutScheme:
    deleted_category = (
        db.query(CategoryModel)
        .filter(
            CategoryModel.id == category_id,
            CategoryModel.deleted_at.isnot(None)).first()
    )

    if not deleted_category:
        raise HTTPException(status_code=404, detail="This Category is not deleted or was not found in the database!")

    deleted_category.updated_at = datetime.now()
    deleted_category.deleted_at = None
    db.commit()
    db.refresh(deleted_category)

    return deleted_category


@categories_router.patch("/update/{category_id}", status_code=200, response_model=CategoryOutScheme)
def update_category(category_id: UUID, data: CategoryUpdateInScheme,
                    db: Session = Depends(get_db)) -> CategoryUpdateInScheme:
    category = db.query(CategoryModel).filter(CategoryModel.id == category_id,
                                              CategoryModel.deleted_at.is_(None)).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found with the given id.")

    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(category, key, value)

    category.updated_at = datetime.now()
    db.commit()

    return category


@categories_router.delete("/delete/{category_id}", status_code=200, response_model=CategoryOutScheme)
def delete_category(category_id: UUID, db: Session = Depends(get_db)) -> CategoryOutScheme:
    category = db.query(CategoryModel).filter(CategoryModel.id == category_id,
                                              CategoryModel.deleted_at.is_(None)).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found with the given id.")

    category.deleted_at = datetime.now()
    db.commit()

    return category

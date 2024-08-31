from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .models import Category as CategoryModel
from .schemas import CategoryOutput as CategoryOutScheme
from mwu.db import get_db

categories_router = APIRouter(prefix="/categories", tags=["Category"])


@categories_router.get("")
def get_all_categories(db: Session = Depends(get_db)) -> list[CategoryOutScheme | None]:
    categories = db.query(CategoryModel).all()
    return categories

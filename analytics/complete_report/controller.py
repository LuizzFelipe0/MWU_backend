from fastapi import APIRouter

analysis_router = APIRouter(prefix="/analytics", tags=["Analysis"])

"""@analysis_router.get("")
def get_all_categories(db: Session = Depends(get_db)) -> list[CategoryOutScheme | None]:
    categories = db.query(CategoryModel).filter(CategoryModel.deleted_at.is_(None)).all()
    return categories
"""

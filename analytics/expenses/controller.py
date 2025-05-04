from fastapi import APIRouter

analytics_router = APIRouter(prefix="/analytics", tags=["Analytics"])

"""@analytics_router.get("/goals")
def get_all_goals(db: Session = Depends(get_db)) -> list[CategoryOutScheme | None]:
    categories = db.query(CategoryModel).filter(CategoryModel.deleted_at.is_(None)).all()
    return categories
"""

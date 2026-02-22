from sqlalchemy.orm import Session
from mwu.repositories.base_repository import BaseRepository
from .models import CategoryTypes as CategoryTypesModel

class CategoryTypeRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session=session, model=CategoryTypesModel)

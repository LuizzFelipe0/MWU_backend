from sqlalchemy.orm import Session
from mwu.repositories.base_repository import BaseRepository
from .models import User as UserModel

class UserRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session=session, model=UserModel)

    def _get_user_scoped_query(self, is_deleted: bool = False):
        return self._get_query().filter(
            self.model.deleted_at.isnot(None) if is_deleted else self.model.deleted_at.is_(None)
        )

    def get_all_users(self):
        return self._get_user_scoped_query().all()

    def get_all_deleted_users(self):
        return self.db.query(self.model).filter(self.model.deleted_at.isnot(None)).all()
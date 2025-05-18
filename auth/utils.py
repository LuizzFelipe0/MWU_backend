from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from mwu.db import get_db
from user.repository import UserRepository


def get_current_user(x_user_id: str = Header(...), db: Session = Depends(get_db)):
    try:
        user_id = UUID(x_user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    repo = UserRepository(session=db)
    user = repo.get_user_by_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

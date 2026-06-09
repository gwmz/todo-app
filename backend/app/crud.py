from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from . import models, schemas
from .core.security import hash_password


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_id(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: schemas.UserCreate):
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
    hashed = hash_password(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

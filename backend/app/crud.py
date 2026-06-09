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


def get_user_categories(db: Session, user_id: str):
    return db.query(models.Category).filter(models.Category.user_id == user_id).all()


def create_category(db: Session, user_id: str, body: schemas.CategoryCreate):
    cat = models.Category(**body.model_dump(), user_id=user_id)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


def update_category(db: Session, cat_id: str, user_id: str, body: schemas.CategoryCreate):
    cat = db.query(models.Category).filter(
        models.Category.id == cat_id, models.Category.user_id == user_id
    ).first()
    if not cat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    for key, value in body.model_dump().items():
        setattr(cat, key, value)
    db.commit()
    db.refresh(cat)
    return cat


def delete_category(db: Session, cat_id: str, user_id: str):
    cat = db.query(models.Category).filter(
        models.Category.id == cat_id, models.Category.user_id == user_id
    ).first()
    if not cat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    db.delete(cat)
    db.commit()
    return {"ok": True}

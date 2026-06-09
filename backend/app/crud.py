from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from . import models, schemas
from .core.security import hash_password


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_id(db: Session, user_id):
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


def get_user_categories(db: Session, user_id):
    return db.query(models.Category).filter(models.Category.user_id == user_id).all()


def create_category(db: Session, user_id, body: schemas.CategoryCreate):
    cat = models.Category(**body.model_dump(), user_id=user_id)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


def update_category(db: Session, cat_id, user_id, body: schemas.CategoryCreate):
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


def delete_category(db: Session, cat_id, user_id):
    cat = db.query(models.Category).filter(
        models.Category.id == cat_id, models.Category.user_id == user_id
    ).first()
    if not cat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    db.delete(cat)
    db.commit()
    return {"ok": True}


def get_user_tasks(db: Session, user_id, status_filter: str | None = None,
                   priority_filter: str | None = None, category_id: str | None = None,
                   search: str | None = None):
    query = db.query(models.Task).filter(models.Task.user_id == user_id)
    if status_filter:
        query = query.filter(models.Task.status == models.TaskStatus(status_filter))
    if priority_filter:
        query = query.filter(models.Task.priority == models.TaskPriority(priority_filter))
    if category_id:
        query = query.filter(models.Task.category_id == category_id)
    if search:
        like = f"%{search}%"
        query = query.filter(
            models.Task.title.ilike(like) | ((models.Task.description != None) & models.Task.description.ilike(like))
        )
    return query.order_by(models.Task.created_at.desc()).all()


def get_task_by_id(db: Session, task_id, user_id):
    return db.query(models.Task).filter(
        models.Task.id == task_id, models.Task.user_id == user_id
    ).first()


def create_task(db: Session, user_id, body: schemas.TaskCreate):
    task = models.Task(**body.model_dump(exclude={"reminder_enabled"}), user_id=user_id, reminder_enabled=body.reminder_enabled)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(db: Session, task_id, user_id, body: schemas.TaskUpdate):
    task = get_task_by_id(db, task_id, user_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    update_data = body.model_dump(exclude_unset=True)
    if body.status == models.TaskStatus.DONE and task.status != models.TaskStatus.DONE:
        update_data["completed_at"] = datetime.utcnow()
    for key, value in update_data.items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id, user_id):
    task = get_task_by_id(db, task_id, user_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"ok": True}

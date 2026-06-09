from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from ..crud import get_user_tasks, get_task_by_id, create_task, update_task, delete_task
from ..database import get_db
from ..schemas import TaskCreate, TaskUpdate, TaskResponse
from .auth import get_current_user_id

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskResponse])
def list_tasks(
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id),
    status: str | None = Query(None, alias="status"),
    priority: str | None = Query(None, alias="priority"),
    category: str | None = Query(None, alias="category"),
    search: str | None = Query(None),
):
    cat_uuid = UUID(category) if category else None
    return get_user_tasks(db, user_id, status_filter=status, priority_filter=priority,
                          category_id=cat_uuid, search=search)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: UUID, db: Session = Depends(get_db), user_id: UUID = Depends(get_current_user_id)):
    task = get_task_by_id(db, task_id, user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("", response_model=TaskResponse, status_code=201)
def add_task(body: TaskCreate, db: Session = Depends(get_db), user_id: UUID = Depends(get_current_user_id)):
    return create_task(db, user_id, body)


@router.put("/{task_id}", response_model=TaskResponse)
@router.patch("/{task_id}", response_model=TaskResponse)
def edit_task(task_id: UUID, body: TaskUpdate, db: Session = Depends(get_db), user_id: UUID = Depends(get_current_user_id)):
    return update_task(db, task_id, user_id, body)


@router.delete("/{task_id}")
def remove_task(task_id: UUID, db: Session = Depends(get_db), user_id: UUID = Depends(get_current_user_id)):
    return delete_task(db, task_id, user_id)

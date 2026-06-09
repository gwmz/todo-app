from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from ..crud import get_user_tasks, get_task_by_id, create_task, update_task, delete_task
from ..database import get_db
from ..schemas import TaskCreate, TaskUpdate, TaskResponse
from .auth import get_current_user_id

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskResponse])
def list_tasks(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
    status: str | None = Query(None),
    priority: str | None = Query(None),
    category_id: str | None = Query(None),
    search: str | None = Query(None),
):
    return get_user_tasks(db, user_id, status_filter=status, priority_filter=priority,
                          category_id=category_id, search=search)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: str, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    task = get_task_by_id(db, task_id, user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("", response_model=TaskResponse, status_code=201)
def add_task(body: TaskCreate, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    return create_task(db, user_id, body)


@router.put("/{task_id}", response_model=TaskResponse)
def edit_task(task_id: str, body: TaskUpdate, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    return update_task(db, task_id, user_id, body)


@router.delete("/{task_id}")
def remove_task(task_id: str, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    return delete_task(db, task_id, user_id)

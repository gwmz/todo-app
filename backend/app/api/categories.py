from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..crud import get_user_categories, create_category, update_category, delete_category
from ..database import get_db
from ..schemas import CategoryCreate, CategoryResponse
from .auth import get_current_user_id

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[CategoryResponse])
def list_categories(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    return get_user_categories(db, user_id)


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def add_category(
    body: CategoryCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    return create_category(db, user_id, body)


@router.put("/{cat_id}", response_model=CategoryResponse)
def edit_category(
    cat_id: str,
    body: CategoryCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    return update_category(db, cat_id, user_id, body)


@router.delete("/{cat_id}")
def remove_category(
    cat_id: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    return delete_category(db, cat_id, user_id)

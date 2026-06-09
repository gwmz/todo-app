from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from .models import TaskStatus, TaskPriority


# ---- Auth ----

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    email: Optional[str] = Field(None, max_length=120)


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: str
    username: str
    email: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---- Category ----

class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    color: str = Field(default="#6366f1", pattern=r"^#[0-9a-fA-F]{6}$")


class CategoryResponse(BaseModel):
    id: str
    name: str
    color: str
    user_id: str
    created_at: datetime

    class Config:
        from_attributes = True


# ---- Task ----

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None
    reminder_enabled: bool = False
    category_id: Optional[str] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    reminder_enabled: Optional[bool] = None
    category_id: Optional[str] = None


class TaskResponse(TaskBase):
    id: str
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    user_id: str
    category: Optional[CategoryResponse] = None

    class Config:
        from_attributes = True

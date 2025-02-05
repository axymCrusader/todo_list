from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class TaskTypeBase(BaseModel):
    name: str

class TaskTypeCreate(TaskTypeBase):
    pass

class TaskTypeResponse(TaskTypeBase):
    id: UUID
    user_id: UUID

    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    task_type_id: UUID

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    task_type_id: Optional[UUID] = None

class TaskResponse(TaskBase):
    id: UUID
    is_completed: bool
    user_id: UUID
    task_type: TaskTypeResponse

    class Config:
        from_attributes = True

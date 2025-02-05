from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.auth.dependencies import get_current_user
from src.auth.models import Basic_User as User
from src.todo_list.schemas import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskTypeCreate,
    TaskTypeResponse
)
from src.todo_list.service import TodoService

router = APIRouter(
    prefix="/todo",
    tags=["todo"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/types", response_model=TaskTypeResponse)
async def create_task_type(
    task_type_data: TaskTypeCreate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    return await TodoService.create_task_type(user, task_type_data, session)

@router.get("/types", response_model=list[TaskTypeResponse])
async def get_task_types(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    return await TodoService.get_user_task_types(user, session)

@router.post("/tasks", response_model=TaskResponse)
async def create_task(
    task_data: TaskCreate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    return await TodoService.create_task(user, task_data, session)

@router.get("/tasks", response_model=list[TaskResponse])
async def get_tasks(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    return await TodoService.get_user_tasks(user, session)

@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: UUID,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    return await TodoService.get_task(task_id, user, session)

@router.patch("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    return await TodoService.update_task(task_id, user, task_data, session)

@router.delete("/tasks/{task_id}")
async def delete_task(
    task_id: UUID,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    await TodoService.delete_task(task_id, user, session)
    return {"status": "success"}

@router.delete("/types/{task_type_id}")
async def delete_task_type(
    task_type_id: UUID,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    await TodoService.delete_task_type(task_type_id, user, session)
    return {"status": "success"}

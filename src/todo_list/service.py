from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.todo_list.models import Task, TaskType
from src.todo_list.schemas import TaskCreate, TaskUpdate, TaskTypeCreate
from src.auth.models import Basic_User as User
from src.todo_list.exceptions import task_not_found, task_type_not_found, not_task_owner

class TodoService:
    @staticmethod
    async def create_task_type(
        user: User,
        task_type_data: TaskTypeCreate,
        session: AsyncSession
    ) -> TaskType:
        task_type = TaskType(
            name=task_type_data.name,
            user_id=user.id
        )
        session.add(task_type)
        await session.commit()
        await session.refresh(task_type)
        return task_type

    @staticmethod
    async def get_user_task_types(
        user: User,
        session: AsyncSession
    ) -> list[TaskType]:
        query = select(TaskType).where(TaskType.user_id == user.id)
        result = await session.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def create_task(
        user: User,
        task_data: TaskCreate,
        session: AsyncSession
    ) -> Task:
        task_type = await session.get(TaskType, task_data.task_type_id)
        if not task_type or task_type.user_id != user.id:
            raise task_type_not_found

        task = Task(
            title=task_data.title,
            description=task_data.description,
            user_id=user.id,
            task_type_id=task_data.task_type_id
        )
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task

    @staticmethod
    async def get_user_tasks(
        user: User,
        session: AsyncSession
    ) -> list[Task]:
        query = (
            select(Task)
            .where(Task.user_id == user.id)
            .options(joinedload(Task.task_type))
        )
        result = await session.execute(query)
        return list(result.unique().scalars().all())

    @staticmethod
    async def get_task(
        task_id: UUID,
        user: User,
        session: AsyncSession
    ) -> Task:
        task = await session.get(Task, task_id)
        if not task:
            raise task_not_found
        if task.user_id != user.id:
            raise not_task_owner
        return task

    @staticmethod
    async def update_task(
        task_id: UUID,
        user: User,
        task_data: TaskUpdate,
        session: AsyncSession
    ) -> Task:
        task = await TodoService.get_task(task_id, user, session)
        
        if task_data.task_type_id:
            task_type = await session.get(TaskType, task_data.task_type_id)
            if not task_type or task_type.user_id != user.id:
                raise task_type_not_found

        update_data = task_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(task, key, value)

        await session.commit()
        await session.refresh(task)
        return task

    @staticmethod
    async def delete_task(
        task_id: UUID,
        user: User,
        session: AsyncSession
    ) -> None:
        task = await TodoService.get_task(task_id, user, session)
        await session.delete(task)
        await session.commit()

    @staticmethod
    async def delete_task_type(
        task_type_id: UUID,
        user: User,
        session: AsyncSession
    ) -> None:
        task_type = await session.get(TaskType, task_type_id)
        if not task_type:
            raise task_type_not_found
        if task_type.user_id != user.id:
            raise not_task_owner
            
        await session.delete(task_type)
        await session.commit()

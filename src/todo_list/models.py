from uuid import UUID
import uuid
from sqlalchemy import String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID

from src.database import Base
from src.auth.models import Basic_User

class TaskType(Base):
    id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    user_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("basic_user.id", ondelete="CASCADE"),
        nullable=False
    )
    
    user: Mapped["Basic_User"] = relationship()
    tasks: Mapped[list["Task"]] = relationship(back_populates="task_type")

class Task(Base):
    id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )
    description: Mapped[str] = mapped_column(
        String(1000),
        nullable=True
    )
    is_completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    user_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("basic_user.id", ondelete="CASCADE"),
        nullable=False
    )
    task_type_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("tasktype.id", ondelete="CASCADE"),
        nullable=False
    )

    user: Mapped["Basic_User"] = relationship()
    task_type: Mapped["TaskType"] = relationship(back_populates="tasks")

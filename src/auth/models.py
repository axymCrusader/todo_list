from uuid import UUID
from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
import uuid


class Basic_User(Base):
    id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: UUID | None = None
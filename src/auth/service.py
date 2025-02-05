from datetime import datetime, timedelta
from typing import Optional
import jwt
from uuid import UUID
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import Basic_User as User, TokenData
from src.config import settings
from src.auth.exceptions import credentials_exception

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def create_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.JWT_SECRET_KEY, 
            algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    async def get_user_by_email(email: str, session: AsyncSession) -> Optional[User]:
        query = select(User).where(User.email == email)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def create_user(email: str, password: str, session: AsyncSession) -> User:
        user = User(
            email=email,
            password_hash=AuthService.get_password_hash(password)
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    def create_access_token(user_id: UUID) -> str:
        return AuthService.create_token(
            data={"sub": str(user_id), "type": "access"},
            expires_delta=timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        )

    @staticmethod
    def create_refresh_token(user_id: UUID) -> str:
        return AuthService.create_token(
            data={"sub": str(user_id), "type": "refresh"},
            expires_delta=timedelta(minutes=settings.JWT_REFRESH_TOKEN_EXPIRE_MINUTES)
        )

    @staticmethod
    async def verify_token(token: str) -> TokenData:
        try:
            payload = jwt.decode(
                token, 
                settings.JWT_SECRET_KEY, 
                algorithms=[settings.JWT_ALGORITHM]
            )
            user_id: str = payload.get("sub")
            token_type: str = payload.get("type")
            
            if user_id is None:
                raise credentials_exception
                
            return TokenData(user_id=UUID(user_id))
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, ValueError):
            raise credentials_exception

    @staticmethod
    async def get_user_by_id(user_id: UUID, session: AsyncSession) -> Optional[User]:
        return await session.get(User, user_id)

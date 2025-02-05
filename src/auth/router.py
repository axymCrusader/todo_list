from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.auth.schemas import UserCreate, UserResponse
from src.auth.service import AuthService
from src.auth.models import Token, Basic_User as User
from src.auth.dependencies import get_current_user
from src.auth.exceptions import invalid_credentials_exception, email_exists_exception

router = APIRouter(prefix='/auth', tags=['auth'])

@router.post("/register", response_model=UserResponse)
async def register(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_async_session)
):
    if await AuthService.get_user_by_email(user_data.email, session):
        raise email_exists_exception
    
    user = await AuthService.create_user(
        email=user_data.email,
        password=user_data.password,
        session=session
    )
    return user

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session)
):
    user = await AuthService.get_user_by_email(form_data.username, session)
    if not user or not AuthService.verify_password(form_data.password, user.password_hash):
        raise invalid_credentials_exception

    return Token(
        access_token=AuthService.create_access_token(user.id),
        refresh_token=AuthService.create_refresh_token(user.id)
    )

@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str,
    session: AsyncSession = Depends(get_async_session)
):
    token_data = await AuthService.verify_token(refresh_token)
    user = await AuthService.get_user_by_id(token_data.user_id, session)
    if not user:
        raise credentials_exception

    return Token(
        access_token=AuthService.create_access_token(user.id),
        refresh_token=AuthService.create_refresh_token(user.id)
    )

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.auth.service import AuthService
from src.auth.models import Basic_User as User
from src.auth.exceptions import credentials_exception

from src.config import settings
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session)
) -> User:
    token_data = await AuthService.verify_token(token)
    user = await AuthService.get_user_by_id(token_data.user_id, session)
    if user is None:
        raise credentials_exception
    return user

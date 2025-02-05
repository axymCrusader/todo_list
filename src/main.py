from fastapi import FastAPI
from src.config import settings
from fastapi.middleware.cors import CORSMiddleware
from src.auth.router import router as auth_router
from src.todo_list.router import router as todo_router
import sentry_sdk

sentry_sdk.init(
    dsn=settings.SENTRY_URL,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.APP_DEBUG
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=['authorization'],
)

app.include_router(auth_router, prefix=f'{settings.API_PREFIX}')
app.include_router(todo_router, prefix=f'{settings.API_PREFIX}')


@app.get("/")
async def read_root():
    return {'hello'}
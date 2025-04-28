import sys
from core.config import app_settings
from db.db import DBConnector
from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import PlainTextResponse

from .short_url import router as short_url_router
from .auth import router as auth_router

api_router = APIRouter()
api_router.include_router(short_url_router, prefix="/short_url", tags=["Short urls"])
api_router.include_router(auth_router, prefix="/auth", tags=["Security"])
db_connector = DBConnector()


async def check_allowed_ip(request: Request):
    def is_ip_banned(headers):
        is_banned = False
        try:
            # так как "X-REAL-IP" можно получить только из внешней сеи, то в качестве заглушки поставим константу
            # real_ip = headers["X-REAL-IP"]
            real_ip = "localhost"
            is_banned = real_ip in app_settings.black_list
        except KeyError:
            print("IP header not found")
            is_banned = True
        return is_banned

    if is_ip_banned(request.headers):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@api_router.get('/', response_class=PlainTextResponse)
async def root_handler():
    return 'Welcome to Short URL Service (SUS)'


@api_router.get('/info')
async def info_handler():
    """Return basic info"""
    return {'api': 'v1',
            'python': sys.version_info}


@api_router.get('/restart_db', status_code=status.HTTP_200_OK)
async def restart_db():
    """Drop DB and create scheme."""
    await db_connector.restart_db()


@api_router.get('/drop_db', status_code=status.HTTP_200_OK)
async def drop_db():
    """Drop DB."""
    await db_connector.drop_db()


@api_router.get("/ping_db", status_code=status.HTTP_200_OK)
async def ping_db() -> None:
    """Check DB accessibility."""
    conn_flag = await db_connector.ping_db()
    if not conn_flag:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="DB is unavailable")
    return conn_flag

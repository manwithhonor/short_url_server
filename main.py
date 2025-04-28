import asyncio
import uvicorn
from fastapi import FastAPI, Depends

from api import base
from core import config
from db.db import DBConnector

app = FastAPI(title=config.app_settings.app_title,
              docs_url='/api/openapi',
              openapi_url='/api/openapi.json',
              dependencies=[Depends(base.check_allowed_ip)]
              )

app.include_router(base.api_router, prefix="/api")


if __name__ == '__main__':
    db = DBConnector()
    asyncio.run(db.restart_db())
    uvicorn.run('main:app',
                host=config.app_settings.project_host,
                port=config.app_settings.project_port,
                reload=True
                )

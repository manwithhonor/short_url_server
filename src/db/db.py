from core.config import app_settings
from models.base import Base
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


class DBConnector:
    def __init__(self):
        self.engine = create_async_engine(app_settings.database_dsn, echo=True, future=True)
        self.async_session = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    async def get_session(self) -> AsyncSession:
        async with self.async_session() as session:
            yield session

    async def drop_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    async def create_scheme(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def restart_db(self):
        await self.drop_db()
        await self.create_scheme()

    async def ping_db(self):
        async with self.engine.begin() as conn:
            try:
                response = await conn.execute(text('SELECT 1'))
                print(response, "DB is available")
                conn_flag = True
            except Exception as e:
                # [Errno 61] Connection refused
                print(e)
                conn_flag = False
        return conn_flag

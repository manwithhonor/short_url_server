from models.history import History as HistoryModel
from models.short_url import ShortURL as ShortURLModel
from schemas.history import HistoryCreate, HistoryUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Any

from .base import RepositoryDB, CreateSchemaType, ModelType


class RepositoryHistory(RepositoryDB[HistoryModel, HistoryCreate, HistoryUpdate]):
    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self._model(user=obj_in.user, short_url_id=ShortURLModel(id=obj_in.short_url_id).id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_multi(self, db: AsyncSession, *, id: Any, skip=0, limit=100) -> List[ModelType]:
        statement = select(self._model).where(self._model.short_url_id == id).offset(skip).limit(limit)
        results = await db.execute(statement=statement)
        return results.scalars().all()


history_crud = RepositoryHistory(HistoryModel)

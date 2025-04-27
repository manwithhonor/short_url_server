from db.db import Base
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Any, Generic, List, Optional, Type, TypeVar

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class Repository:
    def get(self, *args, **kwargs):
        raise NotImplementedError

    def get_multi(self, *args, **kwargs):
        raise NotImplementedError

    def create(self, *args, **kwargs):
        raise NotImplementedError

    def update(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError


class RepositoryDB(Repository, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self._model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        statement = select(self._model).where(self._model.id == id)
        results = await db.execute(statement=statement)
        return results.scalar_one_or_none()

    async def get_multi(self, db: AsyncSession, *, id: Any, skip=0, limit=100) -> List[ModelType]:
        statement = select(self._model).where(self._model.id == id).offset(skip).limit(limit)
        results = await db.execute(statement=statement)
        return results.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self._model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def false_delete(self, db: AsyncSession, *, id: int) -> bool:
        item = await self.get(db, id)
        item.status = "deleted"
        db.add(item)
        await db.commit()
        return True

    async def delete(self, db: AsyncSession, *, id: int) -> ModelType:
        item = await self.get(db, id)
        if item:
            await db.delete(item)
            await db.commit()
            flag = True
        else:
            flag = False
        return flag

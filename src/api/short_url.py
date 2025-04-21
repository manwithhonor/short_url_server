import uuid
from db.db import DBConnector
from fastapi import APIRouter, Depends, HTTPException, status, Request
from schemas import history as history_schema
from schemas import short_url as short_url_schema
from services.history import history_crud
from services.short_url import short_url_crud
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, List

db_connector = DBConnector()
get_session = db_connector.get_session
router = APIRouter()


@router.post("/", response_model=short_url_schema.ShortURL, status_code=status.HTTP_201_CREATED)
async def create_short_url(*, request: Request,
                           db: AsyncSession = Depends(get_session),
                           entity_in: short_url_schema.ShortURLBase) -> Any:
    """Create new short_url by params."""
    short_url = "http://127.0.0.1:8080/" + str(uuid.uuid4())
    create_data = short_url_schema.ShortURLCreate(full_url=entity_in.full_url,
                                                    short_url=short_url,
                                                    creator=request.headers["user-agent"])
    entity = await short_url_crud.create(db=db, obj_in=create_data)
    return entity


@router.get("/{short_url_id}",
            response_model=short_url_schema.ShortURL,
            status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def get_short_url(*, request: Request,
                        db: AsyncSession = Depends(get_session),
                        short_url_id: int) -> Any:
    """Get short url by ID."""
    entity = await short_url_crud.get(db=db, id=short_url_id)
    if not entity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    elif entity.status == "deleted":
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="Item was deleted test")

    # update history
    create_data = history_schema.HistoryCreate(short_url_id=short_url_id, user=request.headers["user-agent"])
    history_entity = await history_crud.create(db=db, obj_in=create_data)
    return entity


@router.delete("/{short_url_id}")
async def delete_short_url(*, db: AsyncSession = Depends(get_session), short_url_id: int) -> Any:
    """Delete an entity."""
    flag = await short_url_crud.false_delete(db=db, id=short_url_id)
    if not flag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return 'Short url was deleted'


@router.get("/{short_url_id}/history", response_model=List[history_schema.History], status_code=status.HTTP_200_OK)
async def get_history_of_url(*, db: AsyncSession = Depends(get_session), short_url_id: int) -> Any:
    """Get history of short url."""
    entity_list = await history_crud.get_multi(db=db, id=short_url_id)
    if not entity_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return entity_list

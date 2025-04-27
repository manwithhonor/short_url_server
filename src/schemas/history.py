from datetime import datetime

from pydantic import BaseModel


class HistoryBase(BaseModel):
    """Shared properties"""
    short_url_id: int
    user: str


class HistoryCreate(HistoryBase):
    """Properties to receive on history creation"""
    short_url_id: int
    user: str


class HistoryUpdate(HistoryBase):
    """Properties to receive on history update"""
    pass


class HistoryInDBBase(HistoryBase):
    """Properties shared by models stored in DB"""
    id: int
    short_url_id: int
    user: str
    runned_at: datetime

    class Config:
        orm_mode = True


class History(HistoryInDBBase):
    """ Properties to return to client"""
    pass


class HistoryInDB(HistoryInDBBase):
    """Properties stored in DB"""
    pass

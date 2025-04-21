from datetime import datetime

from pydantic import BaseModel


class ShortURLBase(BaseModel):
    """Shared properties"""
    full_url: str


class ShortURLCreate(ShortURLBase):
    """Properties to receive on short_url creation"""
    full_url: str
    creator: str
    short_url: str


class ShortURLUpdate(ShortURLBase):
    """Properties to receive on short_url update"""
    pass


class ShortURLInDBBase(ShortURLBase):
    """Properties shared by models stored in DB"""
    id: int
    full_url: str
    short_url: str
    creator: str
    status: str
    create_date: datetime

    class Config:
        orm_mode = True


class ShortURL(ShortURLInDBBase):
    """ Properties to return to client"""
    pass


class ShortURLInDB(ShortURLInDBBase):
    """Properties stored in DB"""
    pass
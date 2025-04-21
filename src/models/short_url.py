from sqlalchemy import Column, DateTime, func, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class ShortURL(Base):
    __tablename__ = "short_url"

    id = Column(Integer, primary_key=True)
    full_url = Column(String)
    short_url = Column(String, unique=True, nullable=False)
    creator = Column(String)
    status = Column(String, default="active")
    create_date = Column(DateTime, server_default=func.now())
    history = relationship("History", back_populates="short_url")

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return f"ShortUrl(full_url={self.full_url} --> short_url={self.short_url})"

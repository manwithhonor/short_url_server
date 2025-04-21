from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class History(Base):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True)
    short_url_id = Column(ForeignKey("short_url.id"))
    user = Column(String, nullable=False)
    runned_at = Column(DateTime, index=True, default=datetime.utcnow)
    short_url = relationship("ShortURL", back_populates="history", lazy="selectin")

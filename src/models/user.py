from sqlalchemy import Column, Integer, String

from .base import Base


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String, unique=True, nullable=False)
    password = Column(String, unique=False, nullable=False)

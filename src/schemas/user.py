from pydantic import BaseModel


class User(BaseModel):
    user_name: str
    password: str


class UserFromDB(User):
    user_id: int

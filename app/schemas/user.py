from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[int] = None
    password: Optional[int] = None

from pydantic import BaseModel, Field


class UserList(BaseModel):
    email: str
    fullname: str


class UserCreate(UserList):
    password: str 

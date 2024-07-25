from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserList(BaseModel):
    id: int = None
    email: str
    fullname: str
    created_on: Optional[datetime] = None
    status: str = None


class UserCreate(UserList):
    password: str 


class ForgotPassword(BaseModel):
    email: str


class ResetPassword(BaseModel):
    reset_password_token: str
    new_password: str
    confirm_password: str
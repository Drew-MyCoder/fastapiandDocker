from pydantic import BaseModel


class UserUpdate(BaseModel):
    fullname: str


class ChangePassword(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str
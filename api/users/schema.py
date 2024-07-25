from pydantic import BaseModel


class UserUpdate(BaseModel):
    fullname: str
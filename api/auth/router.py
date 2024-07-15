from fastapi import APIRouter, Depends, HTTPException
from api.auth import schema
from api.auth import crud
from api.utils import cryptoUtil

router = APIRouter(
    prefix="/api/v1"
)

@router.post("/auth/register", response_model=schema.UserList)
async def register(user: schema.UserCreate):
    # check if user exists
    result = await crud.find_exist_user(user.email)
    if result:
        raise HTTPException(status_code=404, detail="User already registered.")

    # create new user
    user.password = cryptoUtil.hash_password(user.password)
    await crud.save_user(user)

    return {**user.dict()}
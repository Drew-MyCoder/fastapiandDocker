from fastapi import APIRouter, Depends, status
from api.auth import schema as auth_schema
from api.users import schema as user_schema, crud
from api.utils import jwtUtil

router = APIRouter(
    prefix="/api/v1"
)


@router.get("/user/profile")
async def get_user_profile(current_user: auth_schema.UserList = Depends(
    jwtUtil.get_current_user
)):
    return current_user


@router.patch("/user/profile")
async def update_profile(
    request: user_schema.UserUpdate,
    current_user: auth_schema.UserList = Depends(
    jwtUtil.get_current_user
)):
    # update user info
    await crud.update_user(request, current_user)

    return {
        "status_code": status.HTTP_200_OK,
        "detail": "User updated successfully"
    }


@router.delete("/user/profile")
async def deactivate_account(
    current_user: auth_schema.UserList = Depends(jwtUtil.get_current_active_user)
):
    # delete user
    await crud.deactivate_user(current_user)
    return {
        "status_code": status.HTTP_200_OK,
        "detail": "User account has been deactivated successfully"
    }

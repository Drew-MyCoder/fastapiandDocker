from fastapi import APIRouter, Depends, status, HTTPException, File, UploadFile
from api.auth import schema as auth_schema, crud as auth_crud
from api.users import schema as user_schema, crud as user_crud
from api.utils import jwtUtil, cryptoUtil
import os
from PIL import Image
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
    await user_crud.update_user(request, current_user)

    return {
        "status_code": status.HTTP_200_OK,
        "detail": "User updated successfully"
    }


@router.delete("/user/profile")
async def deactivate_account(
    current_user: auth_schema.UserList = Depends(jwtUtil.get_current_active_user)
):
    # delete user
    await user_crud.deactivate_user(current_user)
    return {
        "status_code": status.HTTP_200_OK,
        "detail": "User account has been deactivated successfully"
    }


@router.patch("/user/change-password")
async def change_password(
    change_password_object: user_schema.ChangePassword,
    current_user: auth_schema.UserList = Depends(
        jwtUtil.get_current_user
)
):
     # check if user exists
    result = await auth_crud.find_exist_user(current_user.email)
    if not result:
        # raise HTTPException(status_code=404, detail="User already registered.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # verify current password
    user = auth_schema.UserCreate(**result)
    valid = cryptoUtil.verify_password(change_password_object.current_password, user.password)
    if not valid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Current password is not correct")

    # check new password matches with confirm password
    if change_password_object.new_password != change_password_object.confirm_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="New passwords must match")

    # change password
    change_password_object.new_password = cryptoUtil.hash_password(
        change_password_object.new_password
    )
    await user_crud.change_password(change_password_object, current_user)
    return {
        "status_code": status.HTTP_200_OK,
        "detail": "Password has been changed successfully"
    }


@router.get("/user/logout")
async def logout(
    token: str = Depends(jwtUtil.get_user_token),
    current_user: auth_schema.UserList = Depends(jwtUtil.get_current_active_user)
):
    # save token of user to table blacklist
    await user_crud.save_blacklist_token(token, current_user)
    return {
        "status_code": status.HTTP_200_OK,
        "detail": "User logged out successfully"
    }


@router.patch("/user/upload-profile-image")
async def upload_profile_image(
    file: UploadFile = File(...),
    current_user: auth_schema.UserList = Depends(jwtUtil.get_current_active_user)
):
    try:
        cwd = os.getcwd()
        path_image_dir = "upload-images/user/profile/" + str(current_user.id) + "/"
        full_image_path = os.path.join(cwd, path_image_dir, file.filename)

        print(full_image_path)

        # create directory if it does not exist
        if not os.path.exists(path_image_dir):
            os.mkdir(path_image_dir)

        # rename file to 'profile.png'
        file_name = full_image_path.replace(file.filename, "profile.png")

        # write file
        with open(file_name, 'wb+') as f:
            f.write(file.file.read())
            f.flush()
            f.close()

        return {
            "profile_image": os.path.join(path_image_dir, "profile.png")
        }

    except Exception as e:
        print(e)


@router.get("/user/upload-profile-image")
async def get_profile_image(
    current_user: auth_schema.UserList = Depends(jwtUtil.get_current_active_user)
):
    try:
        cwd = os.getcwd()
        path_image_dir = "upload-images/user/profile/" + str(current_user.id) + "/"
        full_image_path = os.path.join(cwd, path_image_dir, "profile.png")

        # check if image exists
        if os.path.exists(full_image_path):
            # resize profile to 400x400
            image = Image.open(full_image_path)
            image.thumbnail((400, 400))

        return {
            "profile_image": os.path.join(path_image_dir, "profile_400x400.png")
        }

    except Exception as e:
        print(e)
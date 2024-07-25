import jwt
from jwt import PyJWTError
from pydantic import ValidationError
from datetime import datetime, timedelta
from api.utils import constantUtil
from api.auth import crud, schema
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


async def create_access_token(
    *, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=constantUtil.ACCESS_TOKEN_EXPIRE_MINUTE)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, constantUtil.SECRET_KEY, algorithm=constantUtil.ALGORITHM_HS256)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, constantUtil.SECRET_KEY, algorithms=[constantUtil.ALGORITHM_HS256])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        # check if user exist
        result = await crud.find_exist_user(username)
        if not result:
            raise HTTPException(
                status_code=404, 
                detail="User not registered.")
            
        return schema.UserList(**result)


    except (PyJWTError, ValidationError):
        raise credentials_exception


def get_current_active_user(current_user: schema.UserList = Depends(
    get_current_user
)):
    if current_user.status != "1":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail="inactive user")

    return current_user

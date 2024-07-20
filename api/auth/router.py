from fastapi import APIRouter, Depends, HTTPException
from api.auth import schema
from api.auth import crud
from api.utils import cryptoUtil, jwtUtil, constantUtil, emailUtil
from fastapi.security import OAuth2PasswordRequestForm
import uuid

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


@router.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    #  check if user is registered
    result = await crud.find_exist_user(form_data.username)
    if not result:
        raise HTTPException(
            status_code=404, 
            detail="User not registered.")

    # verify password
    user = schema.UserCreate(**result)
    verified_password = cryptoUtil.verify_password(
        form_data.password, user.password)
    if not verified_password:
        raise HTTPException(
            status_code=404, 
            detail="Incorrect username or password")

    # create token
    access_token_expires = jwtUtil.timedelta(
        minutes=constantUtil.ACCESS_TOKEN_EXPIRE_MINUTE)
    access_token = await jwtUtil.create_access_token(
        data={"sub": form_data.username},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_info": {
            "email": user.email,
            "fullname": user.fullname
        }
    }


@router.post("/auth/forgot-password")
async def forgot_password(request: schema.ForgotPassword):
    # check user is registered
    result = await crud.find_exist_user(request.email)
    if not result:
        raise HTTPException(
            status_code=404, 
            detail="User not registered.")

    # create reset code and save in database
    reset_code = str(uuid.uuid1())
    await crud.create_reset_code(request.email, reset_code)

    # sending email
    subject = "Hello Coder"
    recipient = [request.email]
    message = """
    <!DOCTYPE html>
    <html>
    <title>Reset Password</title>
    <body>
    <div style="width:100%;font-family: monospace;">
        <h1>Hello, {0:}</h1>
        <p>Someone has requested a link to reset your password. If you requested this, you can change your password through the button below.</p>
        <a href="http://127.0.0.1:8000/user/forgot-password?reset_password_token={1:}" style="box-sizing:border-box;border-color:#1f8feb;text-decoration:none;background-color:#1f8feb;border:solid 1px #1f8feb;border-radius:4px;color:#ffffff;font-size:16px;font-weight:bold;margin:0;padding:12px 24px;text-transform:capitalize;display:inline-block" target="_blank">Reset Your Password</a>
        <p>If you didn't request this, you can ignore this email.</p>
        <p>Your password won't change until you access the link above and create a new one.</p>
    </div>
    </body>
    </html>
    """.format(request.email, reset_code)
    # enable after filling mail info in .env file
    # await emailUtil.send_email(subject, recipient, message)

    return {
        "reset_code": reset_code,
        "code": 200,
        "message": "We've sent an email with instructions to reset your password."
    }
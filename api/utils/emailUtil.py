from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from starlette.config import Config
from starlette.responses import JSONResponse
from typing import List
# from api import dot_env


# config = Config('.env')

conf = ConnectionConfig(
    MAIL_USERNAME ="username",
    MAIL_PASSWORD = "**********",
    MAIL_FROM = "test@email.com",
    MAIL_PORT = 465,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)
print("=======================")
# print(conf("MAIL_PORT"))
print("=======================")


async def send_email(
    subject: str, 
    recipient: List, 
    message: str) -> JSONResponse:
    message = MessageSchema(
        subject=subject,
        recipients=recipient,
        body=message,
        subtype=MessageType.html
    )
    print(message)
    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(
        status_code=200,
        content={"message": "email has been sent"}
    )
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from api.utils.dbUtil import database
from api.auth import router as auth_router
from api.users import router as user_router
from api.otps import router as otp_router
from api.exceptions.business import BusinessException

app = FastAPI(
    docs_url="/docs",
    redoc_url="/redocs",
    title="FastAPI (Python)",
    description="FastAPI Framework, learning otp, email verifcation, jwt etc",
    version="1.0",
    openapi_url="/openapi.json",
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.exception_handler(BusinessException)
async def business_exception_handler(request: Request, e: BusinessException):
    return JSONResponse(
        status_code=418,
        content={
            "code": e.status_code, 
            "message": e.detail
        }
    )


app.include_router(auth_router.router, tags=["Auth"])
app.include_router(user_router.router, tags=["Users"])
app.include_router(otp_router.router, tags=["OTPs"])
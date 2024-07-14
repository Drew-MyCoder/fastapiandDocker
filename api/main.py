from fastapi import FastAPI
from api.utils.dbUtil import database

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


@app.get('/hello')
def hello():
    return 'hello world drew@@'
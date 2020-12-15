from fastapi import FastAPI, Request, status
from routers import login_router

app = FastAPI()

app.include_router(
  login_router.router,
  prefix="/login",
  tags=["login"]
)
from fastapi import FastAPI, Request, status
from routers import login_router, signup_router, enterprises_router
from utils.jwt_utils import verifyJWT
from dependencies import jwt_dependencies

app = FastAPI()

app.include_router(
  login_router.router,
  prefix="/login",
  tags=["login"]
)

app.include_router(
  enterprises_router.router,
  prefix="/enterprises",
  tags=["enterprises"],
)

app.include_router(
  signup_router.router,
  prefix="/signup",
  tags=["signup"]
)

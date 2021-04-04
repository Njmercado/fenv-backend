from fastapi import FastAPI, Request, status
from routers import login_router, signup_router, enterprises_router, project_router, envs_router, keys_router, user_router
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
  project_router.router,
  prefix="/projects",
  tags=["projects"],
)

app.include_router(
  envs_router.router,
  prefix="/envs",
  tags=["envs"]
)

app.include_router(
  keys_router.router,
  prefix="/keys",
  tags=["keys"]
)

app.include_router(
  signup_router.router,
  prefix="/signup",
  tags=["signup"]
)

app.include_router(
  user_router.router,
  prefix="/user",
  tags=["user"]
)

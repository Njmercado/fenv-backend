from fastapi import APIRouter, Depends
from dependencies.jwt_dependencies import jwtAccess
from utils.queries.env_consumer import createEnv, getEnv, getEnvs
import uuid

router = APIRouter()

@router.post("/")
def createEnvEndpoint(enterprise_id: str, project_id: str, env_name: str, jwt_response: dict = Depends(jwtAccess)):

  try:
    enterprise_id = uuid.UUID(enterprise_id)
    project_id = uuid.UUID(project_id)
    response = createEnv(
      user_email = jwt_response["data"]["email"],
      enterprise_id = enterprise_id,
      project_id = project_id,
      env_name = env_name
    )
    return response
  except Exception as error:
    return { "message": f"Some error has happend: {error}", "error": True }

@router.get("/all")
def getAllEnv(enterprise_id: str, project_id: str, jwt_response: dict = Depends(jwtAccess)):
  
  try:
    user_email = jwt_response["data"]["email"]
    enterprise_id = uuid.UUID(enterprise_id)
    project_id = uuid.UUID(project_id)
    envs = getEnvs(enterprise_id=enterprise_id, project_id=project_id, user_email = user_email)
    return envs 
  except Exception as error:
    return { "message": f"Some error has happend: {error}", "error": True}

@router.get("/only")
def getOneEnv(enterprise_id: str, project_id: str, env_id: str, jwt_response: dict = Depends(jwtAccess)):
  try:
    user_email = jwt_response["data"]["email"]
    enterprise_id = uuid.UUID(enterprise_id)
    project_id = uuid.UUID(project_id)
    env_id = uuid.UUID(env_id)
    project = getEnv(enterprise_id=enterprise_id, project_id=project_id, env_id=env_id, user_email=user_email)
    return project
  except Exception as error:
    return {"message": f"Some error has happend: {error}", "error": True}

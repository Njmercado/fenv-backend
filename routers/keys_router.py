from fastapi import APIRouter, Depends
from dependencies.jwt_dependencies import jwtAccess
from utils.queries.key_consumer import createKey, getKeys, getKey, deleteKey
import uuid

router = APIRouter()

@router.post("/")
def createKeyEndpoint(
  enterprise_id: str,
  project_id: str,
  env_id: str,
  key_name: str,
  key_value: str,
  jwt_response: dict = Depends(jwtAccess)
):
  try:
    enterprise_id = uuid.UUID(enterprise_id)
    project_id = uuid.UUID(project_id)
    env_id = uuid.UUID(env_id)
    response = createKey(
      user_email = jwt_response["data"]["email"],
      enterprise_id = enterprise_id,
      project_id = project_id,
      env_id = env_id,
      key_name = key_name,
      key_value = key_value
    )
    return response
  except Exception as error:
    return { "message": f"Some error has happend: {error}", "error": True }

@router.get("/all")
def getAllKeys(
  enterprise_id: str,
  project_id: str,
  env_id: str,
  jwt_response: dict = Depends(jwtAccess)):
  
  try:
    user_email = jwt_response["data"]["email"]
    enterprise_id = uuid.UUID(enterprise_id)
    project_id = uuid.UUID(project_id)
    envs = getKeys(enterprise_id=enterprise_id, project_id=project_id, env_id=env_id, user_email = user_email)
    return envs 
  except Exception as error:
    return { "message": f"Some error has happend in getAllKeys at keys_router: {error}", "error": True}

@router.get("/only")
def getOneKey(enterprise_id: str, project_id: str, env_id: str, jwt_response: dict = Depends(jwtAccess)):
  try:
    user_email = jwt_response["data"]["email"]
    enterprise_id = uuid.UUID(enterprise_id)
    project_id = uuid.UUID(project_id)
    env_id = uuid.UUID(env_id)
    project = getKey(enterprise_id=enterprise_id, project_id=project_id, env_id=env_id, user_email=user_email)
    return project
  except Exception as error:
    return {"message": f"Some error has happend: {error}", "error": True}

@router.delete("/")
def deleteKeyEndpoint(
  enterprise_id: str, 
  project_id: str,
  env_id: str,
  key_id: str,
  jwt_response: dict = Depends(jwtAccess)
):
  try:
    user_email = jwt_response["data"]["email"]
    enterprise_id = uuid.UUID(enterprise_id)
    project_id = uuid.UUID(project_id)
    env_id = uuid.UUID(env_id)
    key_id = uuid.UUID(key_id)
    response = deleteKey(
      user_email = user_email,
      enterprise_id=enterprise_id,
      project_id = project_id,
      env_id = env_id,
      key_id = key_id,
    )
    return response
  except Exception as error:
    return { "message": f"Some error has happend: {error}", "error": True}

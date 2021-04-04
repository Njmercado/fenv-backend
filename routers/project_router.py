from fastapi import APIRouter, Depends
from dependencies.jwt_dependencies import jwtAccess
from utils.queries.project_consumer import createProject, getProject, getProjects, deleteProject
import uuid

router = APIRouter()

@router.post("/")
def createProjectEndpoint(enterprise_id: str, project_name: str, jwt_response: dict = Depends(jwtAccess)):

  try:
    enterprise_id = uuid.UUID(enterprise_id)
    response = createProject(
      user_email = jwt_response["data"]["email"],
      enterprise_id = enterprise_id,
      project_name = project_name
    )
    return response
  except Exception as error:
    return { "message": f"Some error has happend: {error}", "error": True }

@router.get("/all")
def getAllProjects(enterprise_id: str, jwt_response: dict = Depends(jwtAccess)):
  
  try:
    user_email = jwt_response["data"]["email"]
    enterprise_id = uuid.UUID(enterprise_id)
    projects = getProjects(enterprise_id=enterprise_id, user_email = user_email)
    return projects
  except Exception as error:
    return { "message": f"Some error has happend: {error}", "error": True}

@router.get("/only")
def getOneProject(enterprise_id: str, project_id: str, jwt_response: dict = Depends(jwtAccess)):
  try:
    user_email = jwt_response["data"]["email"]
    enterprise_id = uuid.UUID(enterprise_id)
    project_id = uuid.UUID(project_id)
    project = getProject(enterprise_id=enterprise_id, project_id=project_id, user_email=user_email)
    return project
  except Exception as error:
    return {"message": f"Some error has happend: {error}", "error": True}

@router.delete("/")
def deleteProjectEndpoint(enterprise_id: str, project_id: str, jwt_response: dict = Depends(jwtAccess)):
  try:
    user_email = jwt_response["data"]["email"]
    enterprise_id = uuid.UUID(enterprise_id)
    project_id = uuid.UUID(project_id)
    projects = deleteProject(enterprise_id=enterprise_id, user_email = user_email, project_id = project_id)
    return projects
  except Exception as error:
    return { "message": f"Some error has happend: {error}", "error": True}

from models.user_model import UserModel
from models.enterprise_model import EnterpriseModel
from models.project_model import ProjectModel
from utils.queries.enterprise_consumer import getEnterpriseModel
from utils.queries.user_consumer import getUser
import uuid

def createProject(user_email="", project_name="", enterprise_id: uuid.UUID = uuid.uuid4()):
  try:

    user = getUser(user_email)
    enterprise = getEnterpriseModel(user=user, enterprise_id=enterprise_id)
    if enterprise["error"]:
      return enterprise

    project = ProjectModel(name = project_name)

    enterprise = enterprise["message"]
    enterprise.projects.append(project.id)

    project.save()
    enterprise.save()

    return {"message": "Project created correctly", "error": True}
  except Exception as error:
    return {"message": f"Some error has happend: {error}", "error": True}

def getProjectModel(
  user_email="",
  enterprise_id: uuid.UUID = uuid.uuid4(),
  project_id: uuid.UUID = uuid.uuid4(),
  user: UserModel = None,
  enterprise: EnterpriseModel = None
):
  try:
    if not user: user = getUser(user_email)
    if not enterprise:
      enterprise = getEnterpriseModel(user=user, enterprise_id=enterprise_id)
      if enterprise["error"]: return enterprise
      enterprise = enterprise["message"]

    if project_id in enterprise.projects:
      project = ProjectModel.objects(id = project_id).first()
      return {"message": project, "error": False}
      
  except Exception as error:
    return {"message": f"Some error has happend: {error}", "error": True}

def getProject(
  user_email="",
  enterprise_id: uuid.UUID = uuid.uuid4(),
  project_id: uuid.UUID = uuid.uuid4(),
  user: UserModel = None,
  enterprise: EnterpriseModel = None
):
  try:
    if not user: user = getUser(user_email)
    if not enterprise:
      enterprise = getEnterpriseModel(user=user, enterprise_id=enterprise_id)
      if enterprise["error"]: return enterprise
      enterprise = enterprise["message"]

    if project_id in enterprise.projects:
      project = ProjectModel.objects(id = project_id).aggregate({
        "$project":{
          "id": "$id.uuid",
          "name": 1,
          "created_at": 1 
        }
      })
      return {"message": list(project), "error": False}
      
  except Exception as error:
    return {"message": f"Some error has happend: {error}", "error": True}

def getProjects(user_email="", enterprise_id: uuid.UUID = uuid.uuid4(), user: UserModel = None):
  try:
    if not user: user = getUser(user_email)
    
    enterprise = getEnterpriseModel(user=user, enterprise_id=enterprise_id)
    if enterprise["error"]: return enterprise
    enterprise = enterprise["message"]   

    projects = ProjectModel.objects(id__in = enterprise.projects).aggregate({
      "$project":{
        "id": "$id.uuid",
        "name": 1,
        "created_at": 1,
        "image_src": 1
      }
    })

    return {"message": list(projects), "error": False}

  except Exception as error:
    return {"message": f"Some error has happend: {error}", "error": True}

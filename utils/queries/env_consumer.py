from models.user_model import UserModel
from models.env_model import EnvModel
from models.enterprise_model import EnterpriseModel
from models.project_model import ProjectModel
from utils.queries.enterprise_consumer import getEnterpriseModel
from utils.queries.user_consumer import getUser
from utils.queries.project_consumer import getProjectModel
import uuid

def createEnv(
  user_email="",
  env_name="",
  enterprise_id: uuid.UUID = uuid.uuid4(),
  project_id: uuid.UUID = uuid.uuid4()
):
  try:

    user = getUser(user_email)
    enterprise = getEnterpriseModel(user=user, enterprise_id=enterprise_id)
    if enterprise["error"]: return enterprise
    enterprise = enterprise["message"]

    project = getProjectModel(user=user, enterprise=enterprise, project_id=project_id)
    if project["error"]: return project
    project = project["message"]

    env = EnvModel(name = env_name)
    project.envs.append(env.id)

    env.save()
    project.save()

    return {"message": "Env created correctly", "error": False}
  except Exception as error:
    return {"message": f"Some error has happend: {error}", "error": True}

def getEnv(
  user_email="",
  enterprise_id: uuid.UUID = uuid.uuid4(),
  project_id: uuid.UUID = uuid.uuid4(),
  env_id: uuid.UUID = uuid.uuid4(),
  user: UserModel = None,
  enterprise: EnterpriseModel = None,
  project: ProjectModel = None
):
  try:
    if not user: user = getUser(user_email)

    if not enterprise:
      enterprise = getEnterpriseModel(user=user, enterprise_id=enterprise_id)
      if enterprise["error"]: return enterprise
      enterprise = enterprise["message"]

    if not project:
      project = getProjectModel(user=user, enterprise=enterprise, project_id=project_id)
      if project["error"]: return project
      project = project["message"]

    if env_id in project.envs:
      env = EnvModel.objects(id = env_id).aggregate({
        "$project":{
          "id": "$id.uuid",
          "name": 1,
          "created_at": 1 
        }
      })
      return {"message": list(env), "error": False}
      
  except Exception as error:
    return {"message": f"Some error has happend: {error}", "error": True}

def getEnvs(
  user_email="",
  enterprise_id: uuid.UUID = uuid.uuid4(),
  project_id: uuid.UUID = uuid.uuid4(),
  user: UserModel = None,
  enterprise: EnterpriseModel = None,
  project: ProjectModel = None
):
  try:
    if not user: user = getUser(user_email)

    if not enterprise:
      enterprise = getEnterpriseModel(user = user, enterprise_id = enterprise_id)
      if enterprise["error"]: return enterprise
      enterprise = enterprise["message"]   

    if not project:
      project = getProjectModel(user=user, enterprise=enterprise, project_id=project_id)
      if project["error"]: return project
      project = project["message"]

    envs = EnvModel.objects(id__in = project.envs).aggregate({
      "$project":{
        "id": "$id.uuid",
        "name": 1,
        "created_at": 1,
        "image_src": 1
      }
    })

    return {"message": list(envs), "error": False}

  except Exception as error:
    return {"message": f"Some error has happend: {error}", "error": True}

def getEnvModel(
  user_email="",
  enterprise_id: uuid.UUID = uuid.uuid4(),
  project_id: uuid.UUID = uuid.uuid4(),
  env_id: uuid.UUID = uuid.uuid4(),
  user: UserModel = None,
  enterprise: EnterpriseModel = None,
  project: ProjectModel = None
):
  try:
    if not user: user = getUser(user_email)
    if not enterprise:
      enterprise = getEnterpriseModel(user=user, enterprise_id=enterprise_id)
      if enterprise["error"]: return enterprise
      enterprise = enterprise["message"]
    if not project:
      project = getProjectModel(user=user, enterprise_id=enterprise_id, project_id=project_id)
      if project["error"]: return project
      project = project["message"]

    if env_id in project.envs:
      env = EnvModel.objects(id = env_id).first()
      return {"message": env, "error": False}
      
  except Exception as error:
    return {"message": f"Some error has happend in getEnvModel at env_consumer: {error}", "error": True}

def deleteEnv(
  user_email="",
  enterprise_id: uuid.UUID = uuid.uuid4(),
  project_id: uuid.UUID = uuid.uuid4(),
  env_id: uuid.UUID = uuid.uuid4(),
  user: UserModel = None,
  enterprise: EnterpriseModel = None,
  project: ProjectModel = None
):
  try:
    if not user: user = getUser(user_email)
    if not enterprise:
      enterprise = getEnterpriseModel(user=user, enterprise_id=enterprise_id)
      if enterprise["error"]: return enterprise
      enterprise = enterprise["message"]
    if not project:
      project = getProjectModel(user=user, enterprise=enterprise, project_id=project_id)
      if project["error"]: return project
      project = project["message"]

    if not enterprise_id in user.enterprises: return {"message": "Unable to find this enterprise in your profile", "error": True, "data": None}
    if not project_id in enterprise.projects: return {"message": "Unable to find this project in your profile", "error": True, "data": None}
    if not env_id in project.envs: return {"message": "Unable to find this env in your profile", "error": True, "data": None}

    env = EnvModel.objects.filter(id = env_id).delete()
    env.save()
    
    project.envs.remove(env_id)
    project.save()

    return {"message": "Key deleted correctly", "error": False, "data": None}
  except Exception as error:
    print(f"Some error has happend deleting key at key_consumer.py. error: {error}")
    return {"message": f"Some error has happend: {error}", "error": True}

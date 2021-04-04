from models.user_model import UserModel
from models.env_model import KeyModel, EnvModel
from models.enterprise_model import EnterpriseModel
from models.project_model import ProjectModel
from utils.queries.enterprise_consumer import getEnterpriseModel
from utils.queries.user_consumer import getUser
from utils.queries.project_consumer import getProjectModel
from utils.queries.env_consumer import getEnvModel
from utils.crypto_utils import Cipher
from environs import Env
import uuid
import base64

env = Env()
env.read_env()
key_phrase = bytes(env("CIPHER_KEYPHRASE"), "utf-8")

cipher = Cipher()
cipher.key_phrase = base64.b64decode(key_phrase)

def __cipherData(data):
  formated_data = cipher.addBufferToData(data)
  nonce = cipher.generateNonce()
  crypted_data = cipher.encrypt(formated_data, nonce)   
  final_data = cipher.appendNonceToData(crypted_data, nonce)
  return final_data

def __decipherData(data):
  data = bytes(data, encoding="utf-8")
  decoded_data = base64.b64decode(data)
  data, nonce = cipher.splitCipherData(decoded_data)
  decrypted_data = cipher.decrypt(data, nonce)
  data_without_buffer = cipher.dataWithoutBuffer(decrypted_data)
  return data_without_buffer

def createKey(
  user_email="",
  key_name="",
  key_value="",
  env_id: uuid.UUID = uuid.uuid4(),
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

    env = getEnvModel(user=user, enterprise=enterprise, project=project, env_id=env_id)
    if env["error"]: return env
    env = env["message"]

    ciphered_key_value = __cipherData(key_value)
    key = KeyModel(name = key_name, value=ciphered_key_value)
    env.key_list.append(key)

    env.save()

    return {"message": "Key created correctly", "error": False}
  except Exception as error:
    return {"message": f"Some error has happend in createKey function in key_consumer: {error}", "error": True}

def getKey(
  user_email="",
  enterprise_id: uuid.UUID = uuid.uuid4(),
  project_id: uuid.UUID = uuid.uuid4(),
  env_id: uuid.UUID = uuid.uuid4(),
  key_id: uuid.UUID = uuid.uuid4(),
  user: UserModel = None,
  enterprise: EnterpriseModel = None,
  project: ProjectModel = None,
  env: EnvModel = None
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

    if not env:
      env = getEnvModel(user=user, enterprise=enterprise, project=project, env_id=env_id)
      if env["error"]: return env
      env = env["message"]

    key = env.keys_list.object.filter(id = key_id).aggregate({
        "$project":{
          "id": "$id.uuid",
          "name": 1,
          "created_at": 1 
        }
      })
    key = list(key)
    key_len = len(key)
    if key_len:
      return {"message": None, "error": False, "data": key}
  except Exception as error:
    return {"message": f"Some error has happend: {error}", "error": True}

def getKeys(
  user_email="",
  enterprise_id: uuid.UUID = uuid.uuid4(),
  project_id: uuid.UUID = uuid.uuid4(),
  env_id: uuid.UUID = uuid.uuid4(),
  user: UserModel = None,
  enterprise: EnterpriseModel = None,
  project: ProjectModel = None,
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

    if not env:
      env = getEnvModel(user=user, enterprise=enterprise, project=project, env_id=env_id)
      if env["error"]: return env
      env = env["message"]

    keys = env["message"].key_list

    return {"message": None, "error": False, "data": keys}

  except Exception as error:
    return {"message": f"Some error has happend: {error}", "error": True}

def deleteKey(
  user_email="",
  enterprise_id: uuid.UUID = uuid.uuid4(),
  project_id: uuid.UUID = uuid.uuid4(),
  env_id: uuid.UUID = uuid.uuid4(),
  key_id: uuid.UUID = uuid.uuid4(),
  user: UserModel = None,
  enterprise: EnterpriseModel = None,
  project: ProjectModel = None,
  env: EnvModel = None,
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
    if not env:
      env = getEnvModel(user=user, enterprise=enterprise, project=project, env_id=env_id)
      if env["error"]: return env
      env = env["message"]

    if not enterprise_id in user.enterprises: return {"message": "Unable to find this enterprise in your profile", "error": True, "data": None}
    if not project_id in enterprise.projects: return {"message": "Unable to find this project in your profile", "error": True, "data": None}
    if not env_id in project.envs: return {"message": "Unable to find this env in your profile", "error": True, "data": None}
    if not key_id in env.key_list: return {"message": "Unable to find this key in your profile", "error": True, "data": None}

    env.key_list.objects.filter(id = key_id).delete()
    env.save()
    return {"message": "Key deleted correctly", "error": False, "data": None}
  except Exception as error:
    print(f"Some error has happend deleting key at key_consumer.py. error: {error}")
    return {"message": f"Some error has happend: {error}", "error": True}

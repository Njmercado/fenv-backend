from models.user_model import UserModel
from models.enterprise_model import EnterpriseModel
from utils.queries.user_consumer import getUser
import json
import uuid

def __modelObject2Json(model_object):
  model_object = model_object.to_json()
  model_object = json.loads(model_object)
  return model_object

def createEnterprise(data):
  try:
    user = UserModel.objects(email=data["email"]).first()
    enterprise = EnterpriseModel(name = data["enterprise_name"])
    enterprise.save()

    enterprise_id = str(enterprise.id)
    user.enterprises.append(enterprise_id)

    user.save()
    return {"message": "Enterprise created correctly", "error": False}
  except Exception as error:
    return {"message": f"Some error has happend: {error}", "error": True}

def getEnterpriseModel(user_email="", enterprise_id: uuid.UUID = uuid.uuid4(), user = None):
  try:
    enterprises_ids = []
    if not user: user = getUser(user_email)
    enterprises_ids = user.enterprises

    if enterprise_id in enterprises_ids:
      enterprise = EnterpriseModel.objects(id = enterprise_id).first()
      return {"message": enterprise, "error": False}
    return {"message": None, "error": False}
  except Exception as error:
    return {"message": f"Some error has happend: {error}", "error": True}

def getEnterprise(user_email="", enterprise_id: uuid.UUID = uuid.uuid4(), user = None):
  try:
    enterprises_ids = []
    if not user: user = getUser(user_email)
    enterprises_ids = user.enterprises

    if enterprise_id in enterprises_ids:
      enterprise = EnterpriseModel.objects(id = enterprise_id).aggregate({
        "$project":{
          "id": "$id.uuid",
          "name": 1,
          "created_at": 1 
        }
      })
      return {"message": list(enterprise), "error": False}
    return {"message": None, "error": False}
  except Exception as error:
    return {"message": f"Some error has happend: {error}", "error": True} 

def getEnterprises(user_email):
  try:

    user = getUser(user_email)
    enterprises_ids = user.enterprises

    enterprises = EnterpriseModel.objects.filter(id__in = enterprises_ids).aggregate({
      "$project":{
        "id": "$id.uuid",
        "name": 1,
        "created_at": 1
      }
    })

    return {"message": list(enterprises), "error": False}
  except Exception as error:
    return {"message": f"Some error has happend: {error}", "error": True} 

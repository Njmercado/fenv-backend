from models.user_model import UserModel
from models.enterprise_model import EnterpriseModel

def createEnterprise(data):
  try:
    response = UserModel.objects(email=data["email"]).first()
    enterprise = EnterpriseModel(name = data["enterprise_name"])
    response.enterprises.append(enterprise)
    response.save()
    return {"message": "Enterprise created correctly", "error": False}
  except Exception as error:
    return {"message": f"Some error has happend: {error}", "error": True}

def getEnterprise(data):
  try:
    response = UserModel.objects(email = data["email"]).find(
      {
        "enterprises": {
          "$elemMatch": { "name": data["enterprise_name"], "projects": 0 }
        }
      }
    )

    print(response)
      
    return {"message": "Enterprise created correctly", "error": False}
  except Exception as error:
    return {"message": f"Some error has happend: {error}", "error": True} 

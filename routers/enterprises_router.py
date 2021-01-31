from fastapi import APIRouter, Depends
from dependencies.jwt_dependencies import jwtAccess
from utils.queries.enterprise_consumer import createEnterprise, getEnterprise, getEnterprises
import uuid

router = APIRouter()

@router.post("/")
def createEnterpriseEndpoint(enterprise_name: str, jwt_response: dict = Depends(jwtAccess)):

  try:
    request = {
      "email": jwt_response["data"]["email"],
      "enterprise_name": enterprise_name
    }
    response = createEnterprise(request)
    return response
  except Exception as error:
    return {
      "message": f"Some error has happend: {error}",
      "error": True
    }

@router.get("/only")
def getEnterpriseEndpoint(enterprise_id: str, jwt_response: dict = Depends(jwtAccess)):

  try:
    enterprise_id = uuid.UUID(enterprise_id)
    email = jwt_response["data"]["email"]
    response = getEnterprise(user_email=email, enterprise_id=enterprise_id)
    return response
  except Exception as error:
    return {
      "message": f"Some error has happend: {error}",
      "error": True
    }

@router.get("/all")
def getEnterprisesEndpoint(jwt_response: dict = Depends(jwtAccess)):

  try:
    email = jwt_response["data"]["email"]
    response = getEnterprises(email)
    return response
  except Exception as error:
    return {
      "message": f"Some error has happend: {error}",
      "error": True
    }

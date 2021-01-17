from fastapi import APIRouter, Depends
from dependencies.jwt_dependencies import jwtAccess
from utils.queries.enterprise_consumer import createEnterprise, getEnterprise 

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

@router.get("/")
def getEnterpriseEndpoint(enterprise_name: str, jwt_response: dict = Depends(jwtAccess)):

  try:
    request = {
      "email": jwt_response["data"]["email"],
      "enterprise_name": enterprise_name
    }
    response = getEnterprise(request)
    return response
  except Exception as error:
    return {
      "message": f"Some error has happend: {error}",
      "error": True
    }

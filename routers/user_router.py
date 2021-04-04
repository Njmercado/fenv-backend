from fastapi import APIRouter, HTTPException, Depends
from schemas.login_schema import LoginSchema
from utils.jwt_utils import generateJWT, verifyJWT
from utils.queries.user_consumer import changePassword, changeEmail
from dependencies.jwt_dependencies import jwtAccess

router = APIRouter()

@router.put("/password")
def changePasswordEndpoint(new_password: str, jwt_response: dict = Depends(jwtAccess)):
  try:
    user_email = jwt_response["data"]["email"]
    changePassword(user_email, new_password)

    jwt_schema_as_object = { "email": user_email, "password": new_password }
    new_jwt = generateJWT(jwt_schema_as_object)

    return new_jwt

  except Exception as error:
    return { "message": f"Some error has happend: {error}", "error": True }

@router.put("/email")
def changeEmailEndpoint(new_email: str, jwt_response: dict = Depends(jwtAccess)):
  try:
    old_user_email = jwt_response["data"]["email"]
    password = jwt_response["data"]["password"]
    changeEmail(old_user_email, new_email)

    jwt_schema_as_object = { "email": new_email, "password": password}
    new_jwt = generateJWT(jwt_schema_as_object)

    return new_jwt
  except Exception as error:
    return { "message": f"Some error has happend: {error}", "error": True }

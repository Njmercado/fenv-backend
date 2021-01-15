from fastapi import APIRouter, HTTPException
from schemas.login_schema import LoginSchema
from utils.jwt_utils import generateJWT, verifyJWT
from utils.queries.user_consumer import verifyUser

router = APIRouter()

# Test data

# {
#   "password": "string123_6A",
#   "email": "string@gmail.com"
# }

@router.post("/token")
def login(login_schema: LoginSchema):
  login_schema_as_object = { "email": login_schema.email, "password": login_schema.password }
  try:
    if verifyUser(login_schema_as_object):
      jwt_response = generateJWT(login_schema_as_object)
      return { "message": jwt_response["message"], "error": jwt_response["error"] }
    else:
      return { "message": "Invalid credentials, plis try again", "error": False }
  except Exception as error:
    return { "message": f"Some error has happend: {error}", "error": True }
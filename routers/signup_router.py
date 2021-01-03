from fastapi import APIRouter, HTTPException
from schemas.signup_schema import SignupSchema
from utils.queries import user_consumer
from utils.password import generatePassword

router = APIRouter()

@router.post("/")
def signup(signup_data: SignupSchema):

  try:
    
    response = user_consumer.create_user(signup_data)

    return {
      "message": response["message"],
      "error": response["error"]
    }
  except Exception as error:
    return {
      "message": f"Some error has happend: {error}",
      "error": True
    }

@router.get("/")
def suggestPassword():
  try:
    password = generatePassword(10)

    return {
      "message": password,
      "error": False
    }
  except Exception as error:
    return {
      "message": f"Some error has happend: {error}",
      "error": True
    }
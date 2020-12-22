from fastapi import APIRouter, HTTPException
from schemas.signup_schema import SignupSchema
from utils.queries import user_consumer

router = APIRouter()

@router.post("/")
def signup(signup_data: SignupSchema):

  response = user_consumer.create_user(signup_data)

  return {
    "message": response,
    "error": None
  }
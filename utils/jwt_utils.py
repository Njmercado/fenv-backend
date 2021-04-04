from jose import JWTError, jwt
from environs import Env
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
# from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from utils.queries.user_consumer import verifyUser

env = Env()
env.read_env()

SECRET_KEY = env("SECRET_KEY")
HASH_ALGORITHM = "HS256"

def generateJWT(jwt_data, alive_days=8):
  try:
    day_of_expiration = datetime.utcnow() + timedelta(days=alive_days)
    jwt_data_copy = jwt_data.copy()
    jwt_data_copy.update({ "exp": day_of_expiration })
    encoded_jwt = jwt.encode(jwt_data_copy, SECRET_KEY, algorithm=HASH_ALGORITHM)
    return { "message": None, "error": False, "data": { "jwt": encoded_jwt }}
  except Exception as error:
    print(f"Some error has happend generating the jwt at jwt_utils.py. error: {error}")
    return {"message": f"Some error has happend, error: {error}", "error": True, "data": None}

def verifyJWT(token: str):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[HASH_ALGORITHM])
    if verifyUser(payload):
      return { "message": "Success", "error": False, "data": payload }
    else:
      return {"message": "Some error has happend, are you trying to fuck me?", "error": True}
  except Exception as error:
    return {"message": f"Some error has happend: {error}", "error": True}

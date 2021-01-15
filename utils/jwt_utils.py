from jose import JWTError, jwt
from environs import Env
from datetime import datetime, timedelta

env = Env()
env.read_env()

SECRET_KEY = env("SECRET_KEY")
HASH_ALGORITHM="HS256"

def generateJWT(jwt_data, alive_days=8):
  day_of_expiration = datetime.utcnow() + timedelta(days=alive_days)
  jwt_data_copy = jwt_data.copy()
  jwt_data_copy.update({ "exp": day_of_expiration })
  encoded_jwt = jwt.encode(jwt_data_copy, SECRET_KEY, algorithm=HASH_ALGORITHM)
  return {
    "message": encoded_jwt,
    "error": False
  }

from fastapi import Request, HTTPException, Header
from utils.jwt_utils import verifyJWT

def jwtAccess(token_bearer: str = Header(None)):
  token = token_bearer.split(" ")
  token_data = token[1]
  jwt_response = verifyJWT(token_data)
  if jwt_response["error"]:
    raise HTTPException( status_code=400, detail=jwt_response["message"] ) 
  return jwt_response

from pydantic import BaseModel
from typing import Optional

class LoginSchema(BaseModel):
  password: str
  email: str
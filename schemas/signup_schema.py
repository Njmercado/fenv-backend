from pydantic import BaseModel
from typing import Optional

class SignupSchema(BaseModel):
  name: str
  password: str
  email: str
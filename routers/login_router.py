from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/")
def login():
  return {
    "message": "hola están en login",
    "error": None
  }
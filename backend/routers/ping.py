from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/ping")
def pring():
    return "OK"
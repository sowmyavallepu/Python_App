# Quality gate updated: Coverage 95%, Duplications 45%

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def home():
    return {"message": "Hello World from FastAPI on Azure!"}

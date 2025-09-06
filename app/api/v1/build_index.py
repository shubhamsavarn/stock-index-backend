from fastapi import APIRouter, Query
from app.services.index_service import build_index

router = APIRouter()

@router.post("/build-index")
def build_index_api(start_date: str = Query(...), end_date: str = Query(...)):
    return {"performance": build_index(start_date, end_date)}

from fastapi import APIRouter
from app.models.models import BuildIndexRequest
from app.services.index_builder import build_index
from app.services.performance import get_index_performance
from app.services.composition import get_index_composition, get_composition_changes
from app.services.exporter import export_data


router = APIRouter()

@router.post("/build-index")
def api_build_index(request: BuildIndexRequest):
    return build_index(request.start_date, request.end_date)

@router.get("/index-performance")
def api_index_performance(start_date: str = None, end_date: str = None):
    return get_index_performance(start_date, end_date)

@router.get("/index-composition")
def api_index_composition(date: str):
    return get_index_composition(date)

@router.get("/composition-changes")
def api_composition_changes(start_date: str, end_date: str):
    return get_composition_changes(start_date, end_date)
    @router.post("/export-data")
def api_export_data():
    return export_data()

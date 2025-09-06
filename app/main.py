from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse
from app.models.models import BuildIndexRequest, BuildIndexResponse
from app.services.index_builder import build_index_service, IndexBuildError
from app.services.performance import get_index_performance, PerformanceError
from app.services.composition import get_composition, get_composition_changes, CompositionError
from app.services.exporter import export_data

app = FastAPI()


# ---------------------------
# Exception Handlers
# ---------------------------
@app.exception_handler(IndexBuildError)
async def index_build_exception_handler(request: Request, exc: IndexBuildError):
    return JSONResponse(status_code=400, content={"error": str(exc)})


@app.exception_handler(PerformanceError)
async def performance_exception_handler(request: Request, exc: PerformanceError):
    return JSONResponse(status_code=400, content={"error": str(exc)})


@app.exception_handler(CompositionError)
async def composition_exception_handler(request: Request, exc: CompositionError):
    return JSONResponse(status_code=400, content={"error": str(exc)})


# ---------------------------
# API Endpoints
# ---------------------------
@app.post("/build-index", response_model=BuildIndexResponse)
def build_index_api(start_date: str = Query(...), end_date: str = Query(...)):
    request = BuildIndexRequest(start_date=start_date, end_date=end_date)
    return build_index_service(request)


@app.get("/index-performance")
def performance_api(start_date: str = Query(...), end_date: str = Query(...)):
    return get_index_performance(start_date, end_date)


@app.get("/index-composition")
def composition_api(date: str = Query(...)):
    return get_composition(date)


@app.get("/composition-changes")
def changes_api(start_date: str = Query(...), end_date: str = Query(...)):
    return get_composition_changes(start_date, end_date)


@app.post("/export-data")
def export_api():
    return export_data()

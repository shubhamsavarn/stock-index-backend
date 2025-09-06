from pydantic import BaseModel
from typing import Optional, List

# -------------------------------
# Request models
# -------------------------------
class BuildIndexRequest(BaseModel):
    start_date: Optional[str]
    end_date: Optional[str]

# -------------------------------
# Response models
# -------------------------------
class BuildIndexResponse(BaseModel):
    message: str
    days: int

class IndexPerformanceResponse(BaseModel):
    date: str
    daily_return: float
    cumulative_return: float

class IndexCompositionResponse(BaseModel):
    ticker: str
    weight: float

class CompositionChangeResponse(BaseModel):
    date: str
    entered: List[str]
    exited: List[str]

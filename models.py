from pydantic import BaseModel
from typing import List, Literal, Optional
from datetime import date

class CustomCalendar(BaseModel):
    dates: List[date]

class QuarterlyCalendar(BaseModel):
    initial_date: date

class TopNFilter(BaseModel):
    N: int
    D: str

class ValueFilter(BaseModel):
    P: float
    D: str

class EqualWeighting(BaseModel):
    method: Literal["equal"]

class OptimizedWeighting(BaseModel):
    method: Literal["optimized"]
    D: str
    lb: float
    ub: float

class BacktestRequest(BaseModel):
    calendar_rule: Literal["custom", "quarterly"]
    custom_calendar: Optional[CustomCalendar]
    quarterly_calendar: Optional[QuarterlyCalendar]
    filter_rule: Literal["top_n", "value"]
    top_n_filter: Optional[TopNFilter]
    value_filter: Optional[ValueFilter]
    weighting: dict
    data_path: str


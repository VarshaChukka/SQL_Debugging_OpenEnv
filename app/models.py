from pydantic import BaseModel
from typing import Optional

class Observation(BaseModel):
    problem: str
    db_schema: str
    last_error: Optional[str] = None
    query_result: Optional[str] = None

class Action(BaseModel):
    sql_query: str

class Reward(BaseModel):
    score: float
    feedback: str
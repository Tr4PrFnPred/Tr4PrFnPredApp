"""
    Schemas for /predict endpoint

"""
from typing import Optional, List, Union

from pydantic import BaseModel


class PredictSchema(BaseModel):
    model: str
    sequences: List[Union[str, float]] = []


class PostPredict(BaseModel):
    data: PredictSchema


class PredictResponse(BaseModel):
    model: str
    terms: List[Union[str, float]]


class PredictJobResponse(BaseModel):
    model: Optional[str]
    job_id: int
    status: str = "PENDING"
    terms: Optional[List[Union[str, float]]]

"""
    Schemas for /predict endpoint

"""
from typing import Optional, List, Union

from pydantic import BaseModel, Field


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
    jobId: int
    status: str = "RUNNING"

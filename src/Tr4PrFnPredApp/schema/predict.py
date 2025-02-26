"""
    Schemas for /predict endpoint

"""
from typing import Optional, List, Union, Dict

from pydantic import BaseModel


class PredictSchema(BaseModel):
    model: str
    sequences: Union[str, List[Union[str, float]]]


class PostPredict(BaseModel):
    data: PredictSchema


class PredictResponse(BaseModel):
    model: str
    terms: List[Union[str, float]]


class PredictJobResponse(BaseModel):
    model: Optional[str]
    job_id: Optional[Union[int, str]]
    status: str = "PENDING"
    result: Optional[Dict]
    error: Optional[str]

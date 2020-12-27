import logging

from fastapi import APIRouter
from schema.predict import PostPredict, PredictResponse

from Tr4PrFnPredLib.Pipeline import pipeline


router = APIRouter(
    prefix="/predict",
    tags=["predict"],
    responses={
        200: {"description": "Post successful"}
    },
)


@router.post("/", response_model=PredictResponse)
async def predict_protein_function(json: PostPredict):

    data = json.data
    model_type = data.model
    sequences = data.sequences

    model_pipeline = pipeline(model_type)

    prediction = model_pipeline.predict(sequences)

    res = PredictResponse(model=model_type, terms=prediction)

    return res

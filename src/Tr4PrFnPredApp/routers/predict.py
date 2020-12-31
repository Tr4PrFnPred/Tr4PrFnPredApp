from fastapi import APIRouter
from ..schema.predict import PostPredict, PredictResponse, PredictJobResponse

from Tr4PrFnPredLib.Pipeline import pipeline
from Tr4PrFnPredLib.jobs.submit import submit_job


router = APIRouter(
    prefix="/predict",
    tags=["predict"],
    responses={
        200: {"description": "Post successful"}
    },
)


def _parse_post_predict(json: PostPredict):

    data = json.data
    return data.model, data.sequences


@router.post("/", response_model=PredictResponse)
async def predict_protein_function(json: PostPredict):

    model_type, sequences = _parse_post_predict(json)
    prediction = await pipeline(model_type).predict(sequences)

    res = PredictResponse(model=model_type, terms=prediction)

    return res


@router.post("/job", response_model=PredictJobResponse)
async def submit(json: PostPredict):

    model_type, sequences = _parse_post_predict(json)

    job_id = await submit_job(model_type, sequences)

    res = PredictJobResponse(model=model_type, jobId=job_id)
    return res

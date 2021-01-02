import logging

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from Tr4PrFnPredLib.jobs.submit import check_job_status

from ..schema.predict import PredictJobResponse

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/result",
    tags=["result"],
    responses={
        200: {"description": "Get successful"}
    },
)


@router.get("/page/{job_id}")
async def render_result_page(request: Request, job_id: int):
    return templates.TemplateResponse("result.html", {"request": request, "job_id": job_id})


@router.get("/{job_id}")
async def get_result(job_id: int):

    status = await check_job_status(job_id)

    res = PredictJobResponse(job_id=job_id, status=status)
    return res

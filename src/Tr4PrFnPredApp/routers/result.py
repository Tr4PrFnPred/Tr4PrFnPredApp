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


# FIXME: remove after testing
async def _check_job_status_mock(job_id) -> str:

    from random import randint
    from asyncio import sleep

    status = randint(0, 3)
    await sleep(job_id)
    if status == 0:
        return "COMPLETED"
    elif status == 1:
        return "PENDING"
    else:
        return "RUNNING"


@router.get("/page/{job_id}")
async def render_result_page(request: Request, job_id: int):

    # FIXME: remove after testing
    results = {
        "Q5QJU0": [
            {
                "sequence": "ABCDEFGHIJKLMNOP",
                "term": "GO:0003674",
                "score": "0.999",
                "function_name": "molecular_function"
            },
            {
                "sequence": "QRSTUVWXYZ",
                "term": "GO:0003824",
                "score": "0.872",
                "function_name": "catalytic activity"
            },
        ],
        "QABCDEF": [
            {
                "sequence": "QRSTUVWXYZ",
                "term": "GO:0003824",
                "score": "0.872",
                "function_name": "dihydroceramidase activity"
            },
        ]
    }

    return templates.TemplateResponse("result.html", {"request": request, "job_id": job_id, "results": results})


@router.get("/{job_id}")
async def get_result(job_id: int):

    # status = await check_job_status(job_id)
    # FIXME: Remove after testing
    status = await _check_job_status_mock(job_id)

    res = PredictJobResponse(job_id=job_id, status=status)
    return res

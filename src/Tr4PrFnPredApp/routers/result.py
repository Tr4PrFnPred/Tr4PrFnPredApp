import logging
from typing import Union

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from Tr4PrFnPredLib.jobs.submit import check_job_status
from Tr4PrFnPredLib.jobs.fetch import fetch_results
from Tr4PrFnPredLib.utils.storage import cache_job_id

from ..schema.predict import PredictJobResponse
from ..common.constants import STATE_COMPLETE
from ..common.storage import get_job_status

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

templates = Jinja2Templates(directory="src/Tr4PrFnPredApp/templates/")

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
    await sleep(10)
    if status == 0:
        return "COMPLETED"
    elif status == 1:
        return "PENDING"
    else:
        return "RUNNING"
    # return "COMPLETED"


@router.get("/page/{job_id}")
async def render_result_page(request: Request, job_id: Union[int, str]):

    if get_job_status(job_id) == STATE_COMPLETE:
        status = STATE_COMPLETE
    else:
        status = await check_job_status(job_id)

    logger.info(f'Status {status}')

    if status.upper() == STATE_COMPLETE:

        results = await fetch_results(job_id)

        return templates.TemplateResponse("result.html", {"request": request, "job_id": job_id,
                                                          "status": status,
                                                          "results": zip(results["entries"],
                                                                         results["sequences"], results["terms"]),
                                                          "isComplete": True})

    else:
        return templates.TemplateResponse("result.html", {"request": request, "job_id": job_id, "isComplete": False})


@router.get("/{job_id}")
async def get_results(job_id: Union[str, int]):

    status = await check_job_status(job_id)
    logger.info(f'Get Results: Status: {status}')

    response = PredictJobResponse(job_id=job_id, status=status)

    if status.upper() == STATE_COMPLETE:
        cache_job_id(job_id, STATE_COMPLETE)

    return response


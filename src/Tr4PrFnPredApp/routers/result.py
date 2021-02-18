import logging
from typing import Union

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from Tr4PrFnPredLib.jobs.submit import check_job_status
from Tr4PrFnPredLib.jobs.fetch import fetch_results

from ..schema.predict import PredictJobResponse
from ..common.constants import STATE_COMPLETE

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

    # TODO: consider caching statuses
    status = await check_job_status(job_id)

    logger.info(f'Status {status}')

    if status.upper() == STATE_COMPLETE:
        # FIXME: remove after testing
        entries = ["Q5QJU0", "QABCDEF", "QABCDED", "QABCDEA"]
        sequences = ["ABCDEFGHIJKLMNOP", "QRSTUVWXYZ", "QRSTUVWXYZ", "QRSTUVWXYZ"]
        terms = [{"GO:0003824": "0.999", "GO:0003674": "0.872"}, {"GO:0003824": "0.999"}, {"GO:0003824": 0.768}, {"GO:0003824": 0.896}]

        return templates.TemplateResponse("result.html", {"request": request, "job_id": job_id, "results": zip(entries, sequences, terms), "isComplete": True})
        # return templates.TemplateResponse("result.html", {"request": request, "job_id": job_id, "entries": entries,
        #                                                   "sequences": sequences, "terms": terms})

    else:
        return templates.TemplateResponse("result.html", {"request": request, "job_id": job_id, "isComplete": False})


@router.get("/{job_id}")
async def get_result(job_id: Union[str, int]):

    # status = await check_job_status(job_id)
    # FIXME: Remove after testing
    status = await _check_job_status_mock(job_id)

    res = PredictJobResponse(job_id=job_id, status=status)
    return res

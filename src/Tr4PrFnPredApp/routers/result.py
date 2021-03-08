import aiofiles
import aiofiles.os
import json
import numpy
from typing import Union

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from fastapi import BackgroundTasks

from Tr4PrFnPredLib.jobs.submit import check_job_status
from Tr4PrFnPredLib.jobs.fetch import fetch_results
from Tr4PrFnPredLib.utils.storage import cache_job_id
from Tr4PrFnPredLib.utils.ontology import load_ontology

from ..schema.predict import PredictJobResponse
from ..common.constants import STATE_COMPLETE, STATE_ERROR
from ..common.storage import get_job_status
from ..utils.visualizations import create_d3_network_json_for_terms

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


@router.get("/page/{job_id}")
async def render_result_page(request: Request, job_id: Union[int, str]):

    cached_job_status = get_job_status(job_id)

    if cached_job_status.upper() == STATE_COMPLETE:
        status = STATE_COMPLETE
    elif cached_job_status == STATE_ERROR:
        return {"Error": "Job does not exist"}
    else:
        status = await check_job_status(job_id)

    logger.info(f'Status {status}')

    if status.upper() == STATE_COMPLETE:

        results = await fetch_results(job_id)

        terms_and_score_predictions = results['terms']

        # create d3 network graph json
        all_terms = [list(terms_list.keys()) for terms_list in terms_and_score_predictions]
        go_ont = load_ontology()

        visualizations_json_data = []
        for terms in all_terms:
            nodes, links = create_d3_network_json_for_terms(terms, go_ont)
            visualizations_json_data.append({"nodes": json.dumps(nodes), "links": json.dumps(links)})

        return templates.TemplateResponse("result.html", {"request": request, "job_id": job_id,
                                                          "status": status,
                                                          "results": zip(results["entries"],
                                                                         results["sequences"],
                                                                         terms_and_score_predictions,
                                                                         results["namespaces"],
                                                                         visualizations_json_data),
                                                          "isComplete": True})

    else:
        return templates.TemplateResponse("result.html", {"request": request, "job_id": job_id, "isComplete": False})


@router.get("/{job_id}")
async def get_results(job_id: Union[str, int]):

    status = await check_job_status(job_id)
    logger.info(f'Get Results: Status: {status}')

    response = PredictJobResponse(job_id=job_id, status=status)

    if status.upper() == STATE_COMPLETE:
        # save this status so the next request to this page does not have to recheck the status of job
        cache_job_id(job_id, STATE_COMPLETE)

    return response


class CustomEncoder(json.JSONEncoder):
    """
        Custom JSON encoder to encode numpy types.
    """
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(CustomEncoder, self).default(obj)


async def remove_file_after_download(path: str):
    """
    Background task for the download_results endpoint to delete the temporary file created.

    :param path: Path of file to delete
    """
    await aiofiles.os.remove(path)


@router.get("/download/{job_id}")
async def download_results(job_id: Union[str, int], background_tasks: BackgroundTasks):

    cached_job_status = get_job_status(job_id)

    if cached_job_status.upper() == STATE_COMPLETE:

        results = await fetch_results(job_id)
        response_file_path = f'{job_id}-temp.json'

        background_tasks.add_task(remove_file_after_download, response_file_path)

        # FIXME: Need to return a JSON here but consider just saving results as JSON in future and remove this code
        async with aiofiles.open(response_file_path, "w") as f:
            await f.write(json.dumps(results, cls=CustomEncoder))

        return FileResponse(response_file_path, media_type="application/octet-stream", filename=f'{job_id}.json')
    elif cached_job_status == STATE_ERROR:
        return {"Error": "Job does not exist"}

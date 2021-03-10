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
from ..utils.visualizations import create_d3_network_json_for_terms, create_d3_scatter_json_for_terms

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

templates = Jinja2Templates(directory="src/Tr4PrFnPredApp/templates/")

router = APIRouter(
    prefix="/tr4prfn/result",
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

        # TODO: clean up this code

        terms_and_score_predictions = results['terms']

        # select the go terms with the highest scores for each protein sequence prediction
        terms_and_score_predictions_to_render = []

        for term_and_score_dict in terms_and_score_predictions:
            term_and_score_sorted = dict(sorted(term_and_score_dict.items(), key=lambda item: item[1], reverse=True))
            terms_and_scores_selected = {}
            for i, term in enumerate(term_and_score_sorted):
                if i == 20:  # select the top 20 scores
                    break
                terms_and_scores_selected[term] = term_and_score_sorted[term]
            terms_and_score_predictions_to_render.append(terms_and_scores_selected)

        # create d3 network graph json

        # get the GO terms and remove the scores
        all_terms = list(map(lambda term_and_score: list(term_and_score.keys()), terms_and_score_predictions_to_render))

        # used for traversing the go ontology
        go_ont = load_ontology()

        # create json required for visualizations for each protein sequence GO term predictions
        visualizations_json_data = []
        for i, terms in enumerate(all_terms):
            nodes, links = create_d3_network_json_for_terms(terms, go_ont)
            scatter = create_d3_scatter_json_for_terms(terms_and_score_predictions_to_render)
            visualizations_json_data.append({"nodes": json.dumps(nodes),
                                             "links": json.dumps(links),
                                             "scatter": json.dumps(scatter)})

        return templates.TemplateResponse("result.html", {"request": request, "job_id": job_id,
                                                          "status": status,
                                                          "results": zip(results["entries"],
                                                                         results["sequences"],
                                                                         terms_and_score_predictions_to_render,
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


@router.get("/page/debug/{job_id}")
async def render_result_page_debug(request: Request, job_id: Union[int, str]):

    status = STATE_COMPLETE

    results = {
        "entries": ["AASDG", "JKDJFS"],
        "sequences": ["SDFSJFKSDJFK:LSDF", "SJDFKSJKDSFOISDJFISD"],
        "terms": [{
            "GO:0048706": "0.071314",
            "GO:1904888": "0.620499825",
            "GO:0048701": "0.022626042",
            "GO:0048704": "0.84294938",
            "GO:0060021": "0.015012175"
        }, {
            "GO:0048706": "0.0671314",
            "GO:1904888": "0.020499825",
            "GO:0048701": "0.522626042",
            "GO:0048704": "0.04294938",
            "GO:0060021": "0.915012175"
        }],
        "namespaces": [{
            "GO:0048706": "biological_process",
            "GO:1904888": "biological_process",
            "GO:0048701": "biological_process",
            "GO:0048704": "biological_process",
            "GO:0060021": "biological_process"
        }, {
            "GO:0048706": "molecular_function",
            "GO:1904888": "molecular_function",
            "GO:0048701": "molecular_function",
            "GO:0048704": "molecular_function",
            "GO:0060021": "molecular_function"
        }]
    }

    # TODO: clean up this code

    terms_and_score_predictions = results['terms']

    # select the go terms with the highest scores for each protein sequence prediction
    terms_and_score_predictions_to_render = []

    for term_and_score_dict in terms_and_score_predictions:
        term_and_score_sorted = dict(sorted(term_and_score_dict.items(), key=lambda item: item[1], reverse=True))
        terms_and_scores_selected = {}
        for i, term in enumerate(term_and_score_sorted):
            if i == 20:  # select the top 20 scores
                break
            terms_and_scores_selected[term] = term_and_score_sorted[term]
        terms_and_score_predictions_to_render.append(terms_and_scores_selected)

    # create d3 network graph json

    # get the GO terms and remove the scores
    all_terms = list(map(lambda term_and_score: list(term_and_score.keys()), terms_and_score_predictions_to_render))

    # used for traversing the go ontology
    go_ont = load_ontology()

    # create json required for visualizations for each protein sequence GO term predictions
    visualizations_json_data = []
    print(terms_and_score_predictions_to_render)
    for i, terms in enumerate(all_terms):
        nodes, links = create_d3_network_json_for_terms(terms, go_ont)
        scatter = create_d3_scatter_json_for_terms(terms_and_score_predictions_to_render[i])
        visualizations_json_data.append({"nodes": json.dumps(nodes),
                                         "links": json.dumps(links),
                                         "scatter": json.dumps(scatter)})

    return templates.TemplateResponse("result.html", {"request": request, "job_id": job_id,
                                                      "status": status,
                                                      "results": zip(results["entries"],
                                                                     results["sequences"],
                                                                     terms_and_score_predictions_to_render,
                                                                     results["namespaces"],
                                                                     visualizations_json_data),
                                                      "isComplete": True})
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


def _parse_fasta_input(fasta: str) -> dict:
    """
        The expected input of the protein sequences are in FASTA format.
        http://genetics.bwh.harvard.edu/pph/FASTA.html
        Parse the input to retrieve the entries and sequences.

    :param fasta: the FASTA formatted string.
    :return: Return a dictionary of each entry and its corresponding sequences.
    """

    entry_dict = {}
    entries = fasta.split(">")

    for entry in entries:
        if entry == "":
            continue

        entry_split_by_newline = entry.split("\n")

        if len(entry_split_by_newline) < 1:
            continue

        entry_dict[entry_split_by_newline[0]] = "".join(entry_split_by_newline[1:])

    return entry_dict


@router.post("/", response_model=PredictResponse)
async def predict_protein_function(json: PostPredict):

    model_type, sequences = _parse_post_predict(json)
    prediction = await pipeline(model_type).predict(sequences)

    res = PredictResponse(model=model_type, terms=prediction)

    return res


@router.post("/job", response_model=PredictJobResponse)
async def submit(json: PostPredict):

    model_type, sequences = _parse_post_predict(json)
    entry_dict = _parse_fasta_input(sequences)

    job_id = await submit_job(model_type, entry_dict)

    res = PredictJobResponse(model=model_type, jobId=job_id)
    return res

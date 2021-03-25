from fastapi import APIRouter
from ..schema.predict import PostPredict, PredictJobResponse
from ..common.fasta import CheckEmpty, CheckInvalidCharacters, CheckTags

from Tr4PrFnPredLib.jobs.submit import submit_and_get_job_id
from fastapi import File, UploadFile, Form


router = APIRouter(
    prefix="/tr4prfn/predict",
    tags=["predict"],
    responses={
        200: {"description": "Post successful"}
    },
)


def _parse_post_predict(json: PostPredict):

    data = json.data
    return data.model.lower(), data.sequences


def is_fasta_input(fasta: str) -> bool:

    return CheckEmpty().check_rule(fasta) & CheckTags().check_rule(fasta) & CheckInvalidCharacters().check_rule(fasta)


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
        entry = entry.replace("\r", "")

        entry_split_by_newline = entry.split("\n")

        if len(entry_split_by_newline) < 1:
            continue

        entry_dict[entry_split_by_newline[0]] = "".join(entry_split_by_newline[1:])

    return entry_dict


@router.post("/", response_model=PredictJobResponse)
async def predict_protein_function(json: PostPredict):

    model_type, sequences = _parse_post_predict(json)

    if is_fasta_input(sequences):
        entry_dict = _parse_fasta_input(sequences)

        job_id = await submit_and_get_job_id(model_type, entry_dict)

        res = PredictJobResponse(model=model_type, job_id=job_id, terms=[])

        return res
    else:
        return {"Error": "Invalid FASTA format"}


@router.post("/file", response_model=PredictJobResponse)
async def predict_protein_function_file(model_type: str = Form(...), file: UploadFile = File(...)):
    content = await file.read()

    entry_dict = _parse_fasta_input(content.decode("utf-8"))

    job_id = await submit_and_get_job_id(model_type, entry_dict)

    res = PredictJobResponse(model=model_type, job_id=job_id, terms=[])

    return res

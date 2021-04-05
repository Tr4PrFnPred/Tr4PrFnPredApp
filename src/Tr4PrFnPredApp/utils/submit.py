from Tr4PrFnPredLib.utils.ontology import load_ontology
from Tr4PrFnPredLib.jobs.save import save_results
from Tr4PrFnPredLib.Pipeline import pipeline
from Tr4PrFnPredLib.jobs.submit import cache_job_id
from Tr4PrFnPredLib.common.constants import STATUS_PENDING, STATUS_RUNNING, STATUS_COMPLETE

from ..common.storage import set_local_job

from multiprocessing import Process
import pathlib
import os
import uuid


def create_namespace_list_from_terms(term_collections: list, go_ont) -> list:
    namespace_list = []
    for term_collection in term_collections:
        namespace_collection = {}
        terms = term_collection.keys()

        for term in list(terms):
            try:
                namespace_collection[term] = go_ont.get_namespace(term)
            except:
                continue
        namespace_list.append(namespace_collection)

    return namespace_list


def submit_local_job(model_type, entry_dict):

    # create unique job id
    job_id = str(uuid.uuid4())

    cache_job_id(job_id, STATUS_PENDING, -1)
    set_local_job(job_id)

    p = Process(target=run_prediction_job, args=(model_type, entry_dict, job_id))
    p.start()

    return job_id


def run_prediction_job(model, entry_dict, job_id, folder="./results"):

    cache_job_id(job_id, STATUS_RUNNING)

    if not pathlib.Path(folder).exists():
        os.makedirs(folder)

    results_file = f'{folder}/{job_id}'

    entries = list(entry_dict.keys())
    sequences = list(entry_dict.values())

    go_ont = load_ontology()

    model_pipeline = pipeline(model)
    preds = model_pipeline.predict(sequences, ids=[i for i in range(len(entries))], prot_ids=entries)
    terms_and_score_predictions = list(preds.values())

    namespace_list = create_namespace_list_from_terms(terms_and_score_predictions, go_ont)

    # create dataframe for the results
    results = {
        "entries": entries,
        "sequences": sequences,
        "terms": terms_and_score_predictions,
        "namespaces": namespace_list,
    }

    # next request when job is complete will fetch those results from disk
    save_results(results, results_file)

    cache_job_id(job_id, STATUS_COMPLETE)

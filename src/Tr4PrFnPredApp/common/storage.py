import redis
from .constants import STATE_ERROR


def get_job_status(job_id: str, host="localhost", port=6379) -> str:

    r = redis.Redis(host=host, port=port)

    values = r.hmget(job_id, "status")

    if len(values) == 0:
        # this job does not exist
        job_status = STATE_ERROR
    else:
        job_status = values[0].decode("utf-8")

    return job_status

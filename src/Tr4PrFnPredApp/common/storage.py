import redis


def get_job_status(job_id: str, host="localhost", port=6379) -> str:

    r = redis.Redis(host=host, port=port)

    job_status = r.hmget(job_id, "status")[0].decode("utf-8")

    return job_status

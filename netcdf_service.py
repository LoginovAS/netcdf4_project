from rq import Queue
from rq.job import Job
from redis import Redis
import netcdf_tasks

def create_task(line, file_name):

    redis_conn = Redis();
    queue = Queue(connection = redis_conn)
    job = queue.enqueue('netcdf_tasks.draw_polygon', file_name, line)

    return job.id

def get_task(job_id):
    redis_conn = Redis();
    job = Job.fetch(job_id,connection = redis_conn)

    return job

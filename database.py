import sqlite3
from sqlite3 import Connection
from typing import Dict, List, Tuple
from datetime import datetime
from models import Job, Jobs


def insert_job(connection: Connection, 
               job: Job):
    with connection:
        cur = connection.cursor()
        cur.execute(
            '''
            INSERT INTO jobs (job_name, trigger_type, next_trigger_time)
            VALUES 
            ( :job_name , :trigger_type , :next_trigger_time )
            ;
            ''', 
            job.model_dump()
        )

def get_job(connection: Connection) -> Jobs:

    with connection:
        cur = connection.cursor()
        cur = cur.execute(
            '''
            SELECT job_name, trigger_type, next_trigger_time
            FROM jobs
            ;
            '''
        )
        
        return Jobs(
            jobs = [Job.model_validate(dict(res)) for res in cur]
            )


if __name__ == "__main__":
    DB_PATH = './scheduler.db'

    connection = sqlite3.Connection(database=DB_PATH)
    connection.row_factory = sqlite3.Row
    # test_job = {
    #     'job_name': 'Second job',
    #     'trigger_type': 'CronTrigger()',
    #     'next_trigger_time': datetime(2025,9,8,12,00,00)
    # }

    # insert_job(connection, test_job)
    for job in get_job(connection):
        print(job)
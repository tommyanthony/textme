from rq import Queue, use_connection, Worker, Connection
from redis import Redis
from count_words import count_words_at_url

with Connection(Redis('localhost', 6379)):
    q1 = Queue()
    job1 = q1.enqueue(count_words_at_url, 'http://nvie.com')
    q2 = Queue()
    job2 = q2.enqueue(count_words_at_url, 'http://nvie.com')

#q = Queue(use_connection())
#r = Queue(use_connection())
# Getting the number of jobs in the queue
#q.enqueue(print, 'http://nvie.com')
#r.enqueue(print, 'fucking shit')

# Retrieving jobs
#queued_job_ids = q.job_ids # Gets a list of job IDs from the queue
#queued_jobs = q.jobs # Gets a list of enqueued job instances
#job = q.fetch_job('my_id') # Returns job having ID "my_id"

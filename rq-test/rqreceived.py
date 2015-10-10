from rq import Queue, use_connection, Worker, Connection
from redis import Redis


with Connection(Redis('localhost', 6379)):
    q = Queue()
    w = Worker(q)
    w.work()

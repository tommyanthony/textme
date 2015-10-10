from rq import Queue, Worker, Connection
from redis import Redis
from consts import RQ_HOST, RQ_PORT


def new_worker(host=RQ_HOST, port=RQ_PORT):
    with Connection(Redis(host, port)):
        q = Queue()
        w = Worker(q)
        w.work()

if __name__ == "__main__":
    new_worker()

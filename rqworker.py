from rq import Queue, Connection, Worker
from redis import Redis
from consts import RQ_HOST, RQ_PORT


def new_worker(host=RQ_HOST, port=RQ_PORT):
    with Connection(Redis(host, port)):
        queue = Queue()
        w = Worker(queue)
        w.work()

if __name__ == "__main__":
    new_worker()

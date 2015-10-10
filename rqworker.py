from rq import Queue, use_connection, Worker, Connection
from redis import Redis

HOST = 'localhost'
PORT = 6379


def new_worker(host=HOST, port=PORT):
    with Connection(Redis(host, port)):
        q = Queue()
        w = Worker(q)
        w.work()

if __name__ == "__main__":
    new_worker()

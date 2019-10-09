import redis
import json
import multiprocessing
from worker import Worker


def run_worker(port_id):
    worker = Worker(port_id)
    worker.run()


if __name__ == '__main__':
    multiprocessing.Process(target=run_worker, args=(1, ))
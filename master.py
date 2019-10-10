import redis
import json
import multiprocessing
from worker import Worker


# TODO: lock uuid key on upload
def run_worker():
    worker = Worker()
    worker.run()


if __name__ == '__main__':
    proc = multiprocessing.Process(target=run_worker)
    proc.start()
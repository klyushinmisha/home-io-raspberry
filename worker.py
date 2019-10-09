import redis
import json
from smbus2 import SMBus


class Worker:
    def __init__(self, port_id):
        self.redis = redis.Redis(host='localhost', port=6379, db=0)
        self.port_id = port_id

    def run():
        is_running = True
        with SMBus(self.port_id) as bus:
            while is_running:
                try:
                    block = bus.read_i2c_block_data(80, 0, 16)
                    self.save_telemetry(block)
                except Exception as e:
                    print(e)
                    is_running = False

    def save_telemetry(block):
        r.set('test', block.decode('ascii'))
        rec_data = r.get('test')
        print(rec_data)

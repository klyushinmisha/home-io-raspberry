import redis
import json
import serial


class Worker:
    def __init__(self, port_id):
        self.redis = redis.Redis(host='localhost', port=6379, db=0)
        self.port_id = port_id

    def run():
        ser = serial.Serial(port='/dev/ttyACM0', baudrate=9600)
        while True:
            try:
                out = ser.read(4)
                print(out)
                time.sleep(200)

    def save_telemetry(block):
        r.set('test', block.decode('ascii'))
        rec_data = r.get('test')
        print(rec_data)

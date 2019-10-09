import redis
import json
import serial
import enum


class ProtocolState(enum.Enum):
    INITIAL = 0
    ACK_CONN = 1
    ACK_SERIAL = 2
    ACK_TYPE = 3
    NACK = 4


class Worker:
    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, db=0)

    def run(self):
        self.ser = serial.Serial(port='/dev/ttyACM0', baudrate=9600)
        if not self.init_conn():
            return
        print(self.client_sn, self.client_type)

    def save_telemetry(self, block):
        r.set('test', block.decode('ascii'))
        rec_data = r.get('test')
        print(rec_data)

    def init_conn(self):
        state = ProtocolState.INITIAL
        while True:
            try:
                if state == ProtocolState.INITIAL:
                    msg = self.ser.read(3).decode()
                    if msg == "ACK":
                        self.ser.write('ACK_CONN'.encode())
                        state = ProtocolState.ACK_CONN

                elif state == ProtocolState.ACK_CONN:
                    self.client_sn = self.ser.read(32).decode()
                    self.ser.write('ACK_SERIAL'.encode())
                    state = ProtocolState.ACK_SERIAL

                elif state == ProtocolState.ACK_SERIAL:
                    self.client_type = self.ser.readline.decode()
                    self.ser.write('ACK_TYPE'.encode())
                    state = ProtocolState.ACK_TYPE

                elif state == ProtocolState.ACK_TYPE:
                    return True
            except:
                self.ser.write('NACK'.encode())
                return False

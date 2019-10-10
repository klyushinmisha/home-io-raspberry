import enum
import json
import time

import redis
import serial


class ProtocolState(enum.Enum):
    INITIAL = 0
    ACK_CONN = 1
    ACK_SERIAL = 2
    ACK_TYPE = 3
    NACK = 4


class DeviceTypeEnum(enum.Enum):
    humidity_sensor = 'humidity_sensor'
    blinker = 'blinker'
    rangefinder = 'rangefinder'


class Worker:
    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, db=0)

    def run(self):
        # create serial bus connection
        self.ser = serial.Serial(port='/dev/ttyACM0', baudrate=9600)
        if not self.init_conn():
            return

        # set slave initial data
        slave_data = {
            'type': self.slave_type,
            'enabled': True,
            'telemetry': []
        }
        r.set(self.slave_sn, slave_data)
        while True:
            try:
                self.proc_recieved_data()
                self.send_commands()
            except:
                return

    def proc_recieved_data():
        if self.slave_type == 'humidity_sensor':
            tel = self.ser.read(1).decode()
            self.save_telemetry(tel)
        elif self.slave_type == 'rangefinder':
            tel = self.ser.read(1).decode()
            self.save_telemetry(tel)

    def send_commands():
        # TODO: send commands to end devices
        pass

    def save_telemetry(self, tel):
        slave_cache = r.get(self.slave_sn)
        slave_cache['telemetry'].append(tel)
        r.set(self.slave_sn, slave_cache)

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
                    self.slave_sn = self.ser.read(32).decode()
                    self.ser.write('ACK_SERIAL'.encode())
                    state = ProtocolState.ACK_SERIAL

                elif state == ProtocolState.ACK_SERIAL:
                    self.slave_type = self.ser.readline.decode()
                    self.ser.write('ACK_TYPE'.encode())
                    state = ProtocolState.ACK_TYPE

                elif state == ProtocolState.ACK_TYPE:
                    return True
            except:
                self.ser.write('NACK'.encode())
                return False

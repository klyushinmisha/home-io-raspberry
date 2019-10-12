import enum
import json
import time
import platform

import arrow
import redis
import serial

from redis_dict import to_redis_format, to_python_format


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
        self.settings_db = redis.Redis(host='localhost', port=6379, db=0)
        self.telemetry_db = redis.Redis(host='localhost', port=6379, db=1)
        self.settings_db.flushall()
        self.telemetry_db.flushall()

    def run(self):
        # select unix device file (depends on OS)
        if platform.system() == 'Darwin':
            port='/dev/tty.usbmodem1451'
        elif platform.system() == 'Linux':
            port='/dev/ttyACM0'

        # create serial bus connection
        self.ser = serial.Serial(port=port, baudrate=9600)
        print("Connecting to device...")
        if not self.init_conn():
            return

        print("Ready!")

        # set slave initial data
        slave_settings = {
            'type': self.slave_type,
            'enabled': True
        }
        self.settings_db.hmset(self.slave_sn, to_redis_format(slave_settings))
        while True:
            try:
                self.proc_recieved_data()
                self.send_commands()
                time.sleep(1)
            except Exception as e:
                print(e)
                return

    def proc_recieved_data(self):
        if self.slave_type == 'humidity_sensor':
            tel = self.ser.read(1).decode()
            self.save_telemetry(tel)
        elif self.slave_type == 'rangefinder':
            tel = self.ser.read(1).decode()
            self.save_telemetry(tel)

    def send_commands(self):
        # TODO: send commands to end devices
        pass

    def save_telemetry(self, tel):
        slave_tel = {}
        if self.telemetry_db.exists(self.slave_sn):
            slave_tel = self.telemetry_db.hgetall(self.slave_sn)
        slave_tel[str(arrow.utcnow())] = tel
        self.telemetry_db.hmset(self.slave_sn, slave_tel)

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
                    recieved_type = self.ser.readline().decode()
                    self.slave_type = recieved_type.strip('\r\n')
                    self.ser.write('ACK_TYPE'.encode())
                    state = ProtocolState.ACK_TYPE

                elif state == ProtocolState.ACK_TYPE:
                    return True
            except:
                self.ser.write('NACK'.encode())
                return False

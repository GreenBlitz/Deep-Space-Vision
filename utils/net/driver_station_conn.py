import socket
from .net_consts import *


class DriverStationConn:
    def __init__(self, ip=DRIVER_STATION_IP, port=DRIVER_STATION_PORT):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # udp
        self.client = (ip, port)

    def send(self, msg):
        self.socket.sendto(msg, self.client)

from exceptions import *
from models import *


def init_send_stream(camera, conn):
    conn.set('led_f', False)
    conn.set('led_b', False)
    camera.toggle_auto_exposure(0.75, foreach=True)
    camera.set_exposure(0, foreach=True)


def send_stream(camera, conn):
    camera.read()

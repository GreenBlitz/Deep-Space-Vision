from exceptions import *
from models import *


def init_send_stream(camera, conn, leds):
    leds.off()
    camera.toggle_stream(True, foreach=True)
    camera.toggle_auto_exposure(0.75, foreach=True)


def send_stream(camera, conn):
    camera.read()

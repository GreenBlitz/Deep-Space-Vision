import pigpio as pg


class PGIODevice:
    def __init__(self, port, pi=None):
        if pi is None:
            pi = pg.pi()
            pass
        self.pi = pi
        self.port = port

    def set_power(self, power):
        self.pi.set_PWM_dutycycle(self.port, power)
        pass

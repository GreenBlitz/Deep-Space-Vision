from .pgio_device import PGIODevice


class LedRing(PGIODevice):
    def on(self):
        self.set_power(255)

    def off(self):
        self.set_power(0)

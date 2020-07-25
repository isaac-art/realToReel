import time
from machine import Pin
from machine import ADC

class R2R():
    def __init__(self, speed=95.3, tension=180): 
        self.trigger = 0.1
        self.st = Pin(0, Pin.OUT, value=1)
        self.pl = Pin(4, Pin.OUT, value=1)
        self.ff = Pin(5, Pin.OUT, value=1)
        self.rw = Pin(16, Pin.OUT, value=1)
        self.deviation = 0.2 # +- %
        self.wow_flutter = 0.1 # +-% at 3.75, or 0.08 at 7.5
        self.speed = speed # mm 3.75inch or 190mm/7.5"
        self.tension = tension # mm 7" or large 265mm/10.5"
        self.power = Pin(14, Pin.OUT, value=0)
        self.light_sensor = ADC(0)

    def power_up(self):
        time.sleep(5)
        self.power.on()
        time.sleep(1)
        self.rewind()

    def power_down(self):
        self.stop()
        time.sleep(0.5)
        self.power.off()

    def stop(self):
        self.st.off()
        time.sleep(self.trigger)
        self.st.on()
        time.sleep(1)

    def play(self):
        self.stop()
        self.pl.off()
        time.sleep(self.trigger)
        self.pl.on()

    def rewind(self):
        self.stop() #
        self.rw.off()
        time.sleep(self.trigger)
        self.rw.on()

    def fast_forward(self):
        self.stop() # 
        self.ff.off()
        time.sleep(self.trigger)
        self.ff.on()

    def wait_light_sensor(self):
        # read 0-1024
        threshold = 1020
        while self.light_sensor.read() < threshold:
            time.sleep(0.2)
        return self.stop()


r2r = R2R()
r2r.power_up()
time.sleep(3)
# begin loop
while True:
    r2r.play()
    time.sleep(2) # move past the clear tape
    r2r.wait_light_sensor()
    r2r.rewind()
    time.sleep(2) # move past the clear tape
    r2r.wait_light_sensor()
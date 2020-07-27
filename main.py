import time
from machine import Pin
from machine import ADC

class R2R():
    def __init__(self): 
        #  0, 1, 2, 3, 4, 5, 12, 13, 14, 15, 16,
        print("init")
        self.trigger = 0.1
        self.st = Pin(0, Pin.OUT, value=1)
        self.pl = Pin(4, Pin.OUT, value=1)
        self.ff = Pin(5, Pin.OUT, value=1)
        self.rw = Pin(16, Pin.OUT, value=1)
        self.deviation = 0.2 # +- %
        self.wow_flutter = 0.1 # +-% at 3.75, or 0.08 at 7.5
        self.speed = 95.3 # mm 3.75inch or 190mm/7.5"
        self.tension = 180 # mm 7" or large 265mm/10.5"
        self.power = Pin(14, Pin.OUT, value=0)
        self.light_sensor = ADC(0)
        self.pushbutton = Pin(2, Pin.IN)

    def power_up(self):
        print("powering on")
        time.sleep(0.2)
        self.power.on()
        time.sleep(1)
        self.rewind()
        self.wait_light_sensor()

    def power_down(self):
        print("powering down")
        self.stop()
        time.sleep(0.5)
        self.power.off()

    def stop(self):
        print("stopping")
        self.st.off()
        time.sleep(self.trigger)
        self.st.on()
        time.sleep(1)

    def play(self):
        self.stop()
        print("playing")
        self.pl.off()
        time.sleep(self.trigger)
        self.pl.on()

    def rewind(self):
        self.stop() #
        print("rewinding")
        self.rw.off()
        time.sleep(self.trigger)
        self.rw.on()

    def fast_forward(self):
        self.stop() # 
        print("fast forwarding")
        self.ff.off()
        time.sleep(self.trigger)
        self.ff.on()

    def wait_light_sensor(self):
        print("waiting light sensor")
        # read 0-1024
        threshold = 1020
        while self.light_sensor.read() < threshold:
            time.sleep(0.2)
            if self.pushbutton.value() == 0:
                print("push button interrupt")
                self.power_down()
                return False
        return True

    def wait_pushbutton_on(self):
        print("waiting pushbutton on")
        while self.pushbutton.value() == 1:
            time.sleep(0.25)
        self.power_up()

    def play_rewind_loop(self):
        print("beggining loop")
        play = True
        while play:
            self.play()
            time.sleep(2) # move past the clear tape
            play = self.wait_light_sensor()
            if not play:
                break
            self.rewind()
            time.sleep(2) # move past the clear tape
            play = self.wait_light_sensor()
            if not play:
                break
        return
#

r2r = R2R()
while True:
    r2r.wait_pushbutton_on()
    r2r.play_rewind_loop()
    print("ended")
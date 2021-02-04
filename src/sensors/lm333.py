from gpiozero import LightSensor

class LM333:
    # default pin 8
    def __init__(self, pin=8):
        self.sensor = LightSensor(pin)

    def readData(self):
        #potrebbe servire un 10kOHM per non friggere il raspberry
        return self.sensor.light_detected
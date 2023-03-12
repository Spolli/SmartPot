import RPi.GPIO as GPIO

class Soil_Moisture:
    def __init__(self, pin=7):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin)

    def readData(self):
        return GPIO.input(self.pin)
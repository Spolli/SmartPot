import RPi.GPIO as GPIO

class WaterLever:
    # default pin 9 - 11

    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def readData(self):
        #potrebbe servire un 10kOHM per non friggere il raspberry
        stat = GPIO.input(self.pin)
        return True if stat else False
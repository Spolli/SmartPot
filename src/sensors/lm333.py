import RPi.GPIO as GPIO

class LM333:
    # default pin 8
    def __init__(self, pin=8):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.pin = pin

    def readData(self):
        #potrebbe servire un 10kOHM per non friggere il raspberry
        stat = GPIO.input(self.pin)
        return True if stat else False
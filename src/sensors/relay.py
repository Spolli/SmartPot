import RPi.GPIO as GPIO

class Relay:
    
    pinSetup = {
        'MISC': 21,
        'WATER_WARM': 20,
        'VENT_OUT': 16,
        'VENT_IN': 16,
        'LAMPS': 19,
        'POMPA': 13
    }

    appliance_status = {
        'MISC': GPIO.LOW,
        'WATER_WARM': GPIO.LOW,
        'VENT_OUT': GPIO.LOW,
        'VENT_IN': GPIO.LOW,
        'LAMPS': GPIO.LOW,
        'POMPA': GPIO.LOW
    }

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setmode(GPIO.BOARD)
        for k, v in self.pinSetup.values():
            GPIO.setup(v, GPIO.OUT)

    def turnOn(self, appliance):
        GPIO.output(self.pinSetup[appliance], GPIO.HIGH)
        self.appliance_status[appliance] = GPIO.HIGH

    def turnOff(self, appliance):
        GPIO.output(self.pinSetup[appliance], GPIO.LOW)
        self.appliance_status[appliance] = GPIO.LOW
from gpiozero import LED

class Relay:
    pinSetup = {
        'MISC': 21,
        'WATER_WARM': 20,
        'VENT_OUT': 16,
        'VENT_IN': 16,
        'LAMPS': 19,
        'POMPA': 13
    }

    def __init__(self):
        for k, v in self.pinSetup.values():
            self.ctrl_app[k] = LED(v)

    def turnOn(self, appliance):
        self.ctrl_app[appliance].on()

    def turnOff(self, appliance):
        self.ctrl_app[appliance].off()

    def toggle(self, appliance):
        self.ctrl_app[appliance].toggle()

    def status(self, appliance):
        return self.ctrl_app[appliance].value


from gpiozero import LED

class Relay:
    def __init__(self, pin_number):
        self.reley = LED(pin_number)

    def turnOn(self):
        self.reley.on()

    def turnOff(self):
        self.reley.off()

    def toggle(self):
        self.reley.toggle()

    def status(self):
        return self.reley.value


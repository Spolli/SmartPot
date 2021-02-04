from gpiozero import Button

class WaterLever:
    # default pin 9 - 11

    def __init__(self, pin):
        self.switch = Button(pin)

    def readData(self):
        #potrebbe servire un 10kOHM per non friggere il raspberry
        return not self.switch.is_pressed
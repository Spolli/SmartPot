import Adafruit_DHT

class DHT22:
    # default pin 7
    def __init__(self, pin):
        self.pin = pin
        self.DHT_SENSOR = Adafruit_DHT.DHT22

    def readData(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.DHT_SENSOR, self.pin)
        if humidity is not None and temperature is not None:
            return humidity, temperature
        else
            return None, None
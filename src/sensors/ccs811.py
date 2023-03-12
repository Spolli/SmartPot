import board
import busio
import adafruit_ccs811

class CCS811:
    #dafault pin 2 - 3
    #alimentazione da 3.3v

    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.ccs811 = adafruit_ccs811.CCS811(self.i2c)

    def readData(seld):
        if self.ccs811.data_ready:
            return self.ccs811.eco2, self.ccs811.tvoc
            #CO2: {} PPM, TVOC: {} PPB
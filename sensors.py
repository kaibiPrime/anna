import Adafruit_DHT
import time


class DHT:
    def __init__(self):
        self.dhtSensor = Adafruit_DHT.DHT22
        self.dhtPin = 4

    def getTempHumidity(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.dhtSensor, self.dhtPin)

        if humidity is not None and temperature is not None:
            return [temperature, humidity]
        else: return False
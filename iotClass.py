import requests
import json

class IotDevice():
    """contains general properties of a iot device"""
    def __init__(self, manufacturer, name):
        self.manufacturer = manufacturer
        self.name = name

class attM2x(IotDevice):
    """contains required info for iot deice and a put method"""
    def __init__(self, manufacturer, name, deviceNumber, X_M2X_KEY):
        IotDevice.__init__(self, manufacturer, name)
        self.deviceNumber = deviceNumber
        self.X_M2X_KEY = X_M2X_KEY

    def put_json(self, streamDictionary):
        """put request to input a given value into the att M2X"""
        for streamName, value in streamDictionary.items():
	    url = "http://api-m2x.att.com/v2/devices/" + self.deviceNumber + "/streams/" + streamName + "/value"
            payload = {'value': value}
	    headers = {'X-M2X-KEY': self.X_M2X_KEY,
                   'Content-Type': 'application/json'}
	    print(url)
            response = requests.put(url, data=json.dumps(payload), headers=headers)

#this will be the function that calls this class
# from sense_hat import SenseHat
#find a way to run this function every hour


# sense = SenseHat()
#gets the tempature, humidity, and pressure of an area
# temperature = sense.get_temperature()
# humidity = sense.get_humidity()
# pressure = sense.get_pressure()

# print(temperature)
# print(humidity)
# print(pressure)

# streamDictionary = {'temperature': temperature}# , 'humidity': humidity, 'pressure': pressure}

# m2xSenseHatRasperryPi3 = attM2x("Rarpberry Pi","SenseHat_Raspberry_Py3","04be6de5865d3d9d95a6dbd7182d3083","241bedffb719af49f3b296b783ca5d49")
# m2xSenseHatRasperryPi3.put_json(streamDictionary)

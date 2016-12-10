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
        response = requests.put(url, data=json.dumps(payload), headers=headers)

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
        # TODO Consider changing loop to passing a dictionary in the payload
        for streamName, value in streamDictionary.items():
            url = "http://api-m2x.att.com/v2/devices/" + self.deviceNumber + "/streams/" + streamName + "/value"
            payload = {'value': value}
            headers = {'X-M2X-KEY': self.X_M2X_KEY, 'Content-Type': 'application/json'}
            response = requests.put(url, data=json.dumps(payload), headers=headers)

class ApiManager(IotDevice):
    """
    manages multiple APIs
    """
    def __init__(self, manufacturer, name, api_key):
        IotDevice.__init__(self, manufacturer, name)
        self.api_key = api_key
        self.local_temp_f = None
        self.local_pressure = None
        self.local_relative_humidity = None
        self.alert_type = None

    def set_wunderground_measurement(self, state, city, query):
        response = requests.get("http://api.wunderground.com/api/" + str(self.api_key) + "/" + query + "/q/" +state+ "/"+ city +".json")
        data = response.json()
        if (query == 'conditions'):
            self.local_temp_f = data['current_observation']['local_temp_f']
            self.local_pressure = data['current_observation']['local_pressure_mb']
            self.local_relative_humidity = data['current_observation']['local_relative_humidity']
        elif(query =='alerts'):
            if (data['alerts']):
                self.alert_description = data['alerts'][0]['type']

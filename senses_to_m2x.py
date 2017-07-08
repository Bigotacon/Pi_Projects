from iotClass import IotDevice, attM2x, ApiManager
from sense_hat import SenseHat


def main():
    """this function calls all objects and methods"""
    api_key_dic = {'att_m2x':'241bedffb719af49f3b296b783ca5d49', 'wunderground': 'f8fa5776e55f9681' }
    sense = SenseHat()
    temp = sense.get_temperature()
    hum = sense.get_humidity()
    pressure = sense.get_pressure()
    FACTOR = 5.466

    cpu_temp = ((int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1000) * 1.8 + 32)
    temp  = (temp * 1.8) + 32
    temp_calibrated = temp - ((cpu_temp - temp)/FACTOR)

    api_get = ApiManager('RaspberryPi', 'wunderground_api', api_key_dic['wunderground'])
    api_get.set_wunderground_measurement('RI', 'Tiverton', 'conditions')


    streamDictionary = {'temperature': temp_calibrated, 'humidity': hum,
                        'pressure':pressure,'tiv_temperature':api_get.local_temp_f,
                        'tiv_pressure': api_get.local_pressure, 'tiv_humidity': api_get.local_relative_humidity,
                        'cpu_temp': cpu_temp }
    m2xSenseHatRasperryPi3 = attM2x('Rarpberry Pi',
                                    'SenseHat_Raspberry_Py3',
                                    '04be6de5865d3d9d95a6dbd7182d3083',
                                    api_key_dic['att_m2x'])
    m2xSenseHatRasperryPi3.put_json(streamDictionary)

main()

from iotClass import IotDevice, attM2x
from sense_hat import SenseHat


def main():
    """this function calls all objects and methods"""
    sense = SenseHat()
    temp = sense.get_temperature()
    hum = sense.get_humidity()
    pressure = sense.get_pressure()

    cpu_temp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1000
    FACTOR = 5.466

    temp_calibrated = temp - ((cpu_temp - temp)/FACTOR)
    streamDictionary = {'temperature': temp_calibrated}
    m2xSenseHatRasperryPi3 = attM2x("Rarpberry Pi",
                                    "SenseHat_Raspberry_Py3",
                                    "04be6de5865d3d9d95a6dbd7182d3083",
                                    "241bedffb719af49f3b296b783ca5d49")
    m2xSenseHatRasperryPi3.put_json(streamDictionary)

main()

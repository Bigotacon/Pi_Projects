from iotClass import ApiManager
from twilio.rest import TwilioRestClient
import os

alert_dir = os.path.join(os.path.dirname(__file__), 'alert.txt')
account_sid = "ACc71834cd65de8e2b34c66e45d0b4d061"
auth_token = "9dc3924b2102355d3f65c914e90f6548"
client = TwilioRestClient(account_sid, auth_token)
api_get = ApiManager('RaspberryPi', 'twilio_api', 'f8fa5776e55f9681')
api_get.set_wunderground_measurement('RI', 'Tiverton', 'alerts')

disaster_dic = {
    'HUR':'Hurricane Local Statement',
    'TOR':'Tornado Warning',
    'TOW':'Tornado Watch',
    'WRN':'Severe Thunderstorm Warning',
    'SEW':'Severe Thunderstorm Watch',
    'WIN':'Winter Weather Advisory',
    'FLO':'Flood Warning',
    'WAT':'Flood Watch / Statement',
    'WND':'High Wind Advisory',
    'SVR':'Severe Weather Statement',
    'HEA':'Heat Advisory',
    'FOG':'Dense Fog Advisory',
    'SPE':'Special Weather Statement',
    'FIR':'Fire Weather Advisory',
    'VOL':'Volcanic Activity Statement',
    'HWW':'Hurricane Wind Warning',
    'REC':'Record Set',
    'REP':'Public Reports',
    'PUB':'Public Information Statement',
}

if(api_get.alert_type == None):
    with open(alert_dir, 'w') as w:
        w.write('None')

elif (api_get.alert_type in disaster_dic):
    with open(alert_dir, 'r') as r:
        last_read = r.read()

    if(api_get.alert_type != last_alert):
        message = client.messages.create(to="+14056642575", from_="+14052544690",
                                         body= disaster_dic[api_get.alert_type])
        with open(alert_dir, 'w') as w:
            w.write(str(api_get.alert_type))

import requests
import json
import datetime
import calendar


class IotDevice():

    '''contains general properties of a iot device'''

    def __init__(self, manufacturer, name):
        self.manufacturer = manufacturer
        self.name = name


class attM2x(IotDevice):

    '''contains required info for iot deice and a put method'''

    def __init__(self, manufacturer, name, deviceNumber, X_M2X_KEY):
        IotDevice.__init__(self, manufacturer, name)
        self.deviceNumber = deviceNumber
        self.X_M2X_KEY = X_M2X_KEY

    def put_json(self, streamDictionary):
        '''put request to input a given value into the att M2X'''
        # TODO Consider changing loop to passing a dictionary in the payload
        for streamName, value in streamDictionary.items():
            url = 'http://api-m2x.att.com/v2/devices/' + \
                self.deviceNumber + '/streams/' + streamName + '/value'
            payload = {'value': value}
            headers = {
                'X-M2X-KEY': self.X_M2X_KEY, 'Content-Type': 'application/json'}
            response = requests.put(
                url, data=json.dumps(payload), headers=headers)


class ApiManager(IotDevice):

    '''manages multiple APIs'''

    def __init__(self, manufacturer, name, api_key):
        IotDevice.__init__(self, manufacturer, name)
        self.FLIGHT_API_KEY = api_key
        self.local_temp_f = None
        self.local_pressure = None
        self.local_relative_humidity = None
        self.alert_type = None

    def set_wunderground_measurement(self, state, city, query):
        response = requests.get('http://api.wunderground.com/api/' +
                                str(self.FLIGHT_API_KEY) +
                                '/' + query + '/q/' + state
                                + '/' + city + '.json')
        data = response.json()
        response.url
        if (query == 'conditions'):
            self.local_temp_f = data['current_observation']['local_temp_f']
            self.local_pressure = data[
                'current_observation']['local_pressure_mb']
            self.local_relative_humidity = data[
                'current_observation']['local_relative_humidity']
        elif(query == 'alerts'):
            if (data['alerts']):
                self.alert_description = data['alerts'][0]['type']


class VacationManager(IotDevice):

    '''manages APIs related to vacation found on skyscanner'''

    def __init__(self, manufacturer, name, adults = 2):
        IotDevice.__init__(self, manufacturer, name)
        self.SKYSCANNER_API_URL = 'http://partners.api.skyscanner.net'
        self.FLIGHT_API_KEY = 'jo509986351975384655849688593598'
        self.adults = adults
        self.next_month = self.__add_months(datetime.date.today(), 1)
        self.inbound_carrier = None
        self.outbound_carrier = None
        self.inbound_date = None
        self.outbound_date = None
        self.travel_expenses = 0
        self.hotel_booking_url = None

    def __return_carrier_name(self, data, low_carrier_id):
        for item in data:
            if(low_carrier_id == item['CarrierId']):
                low_carrier_name = item['Name']
                return low_carrier_name

    def __format_unicode_date(self, time):
        then = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S')
        return then.strftime('%Y-%m-%d')
        # return then.strftime('%B %d, %Y %H:%M:%S %p')

    def __add_months(self, sourcedate, months):
        month = sourcedate.month - 1 + months
        year = int(sourcedate.year + month / 12)
        month = month % 12 + 1
        day = min(sourcedate.day, calendar.monthrange(year, month)[1])
        return datetime.date(year, month, day).strftime('%Y-%m')

    def get_airline_skyScanner(self, query, origin_place, destination_place):
        response = requests.get(self.SKYSCANNER_API_URL +
                                '/apiservices/{0}/v1.0/US/USD/en-US/{1}/{2}/{3}/{3}?apiKey={4}'
                                .format(query, origin_place, destination_place,
                                        self.next_month, self.FLIGHT_API_KEY), json={})
        data = response.json()
        i = 0
        lowest = 0
        for item in data:
            if (data['Quotes'][i]['InboundLeg']['DepartureDate'] != data['Quotes'][i]['OutboundLeg']['DepartureDate']):
                if(data['Quotes'][i]['MinPrice'] < data['Quotes'][lowest]['MinPrice']):
                    lowest = i
            i = i + 1
        outbound_low_carrier_id = data['Quotes'][lowest]['OutboundLeg']['CarrierIds']
        inbound_low_carrier_id = data['Quotes'][lowest]['InboundLeg']['CarrierIds']

        self.outbound_carrier = self.__return_carrier_name(data['Carriers'],
                                                         inbound_low_carrier_id[0])
        self.inbound_carrier = self.__return_carrier_name(data['Carriers'],
                                                        outbound_low_carrier_id[0])
        self.travel_expenses = self.travel_expenses + \
            data['Quotes'][lowest]['MinPrice'] * self.adults
        self.outbound_date = (self.__format_unicode_date(
            data['Quotes'][lowest]['OutboundLeg']['DepartureDate']))
        self.inbound_date = (self.__format_unicode_date(
            data['Quotes'][lowest]['InboundLeg']['DepartureDate']))

    def get_hotel_skyScanner(self, city_id, rooms=1):
        guests = self.adults - 1
        HOTEL_API_KEY = 'prtl6749387986743898559646983194'
        hotel_counter = 0
        hotel_id = None
        max_price = 3000

        session = requests.Session()
        response = session.get(self.SKYSCANNER_API_URL
                               +
                               '/apiservices/hotels/liveprices/v2/US/USD/en-US/{0}/{1}/{2}/{3}/{4}/?apiKey={5}'
                               .format(city_id, self.outbound_date, self.inbound_date, guests, rooms, HOTEL_API_KEY))

        # print self.SKYSCANNER_API_URL +'/apiservices/hotels/liveprices/v2/US/USD/en-US/{0}/{1}/{2}/{3}/{4}/?apiKey={5}'.format(city_id, self.outbound_date, self.inbound_date, guests, rooms, HOTEL_API_KEY)
        session_key = response.headers['Location']
        polling_response = requests.get(self.SKYSCANNER_API_URL + session_key
                                        +
                                        '&price=0-{0}&sortColumn=price&sortOrder=asc'
                                        .format(max_price), json={})

        live_prices_data = polling_response.json()

        if (live_prices_data['total_available_hotels'] == 0):
            print 'woops it looks like there is no hotels'
            return

        for item in live_prices_data['hotels']:
            if (item['star_rating'] >= 3 and item['distance_from_search'] < 24):
                hotel_id = item['hotel_id']
                hotel_counter = hotel_counter + 1

        if hotel_counter == 0:
            print 'no qualified hotels'
            return

        detail_url_template = live_prices_data['urls']['hotel_details']
        detail_response = requests.get(self.SKYSCANNER_API_URL + detail_url_template
                                       + '&hotelIds=' + str(hotel_id))

        # print(self.SKYSCANNER_API_URL + detail_url_template
        #       + '&hotelIds=' + str(hotel_id))
        detail_data = detail_response.json()
        # first [i] loops through hotels_prices
        # second[i] loops all agents

        self.travel_expenses = self.travel_expenses + \
            detail_data['hotels_prices'][0]['agent_prices'][0]['price_total']
        self.hotel_booking_url = detail_data['hotels_prices'][
            0]['agent_prices'][0]['booking_deeplink']


    def live_polling(self):
        # from requests import Request, Session
        # session = requests.Session()
        # headers = {'Content-type': 'application/json'}
        # req = Request('POST', 'http://partners.api.skyscanner.net/apiservices/pricing/v1.0', headers=headers)

        from requests import Request, Session
        url = 'http://partners.api.skyscanner.net/apiservices/pricing/v1.0'
        data = {}
        payload = {'apiKey': 'jo509986351975384655849688593598', 'Country': 'US', 'currency': 'USD', 'locale':'en-US', 'originplace': 'OKC', 'destinationplace':'ORD', 'outbounddate': '2017-01-02', 'inbounddate': '2017-01-11', 'adults': '1' }
        headers = {'Content-Type': 'application/json'}
        s = Session()
        req = Request('POST',  url, data=data, headers=headers)
        print(req.headers)


def main():

    vacation_dic = {'Chicago': ['ORD', '95673392'], 'Providence': ['PVD', '95673680'], 'Atlanta': ['ATL','27541735'], 'Seatle': ['SEA', '27538444']}

    for city_name, city_id in vacation_dic.iteritems():
        city_name = VacationManager('RP', 'Skyscanner')
        city_name.get_airline_skyScanner('browsequotes', 'OKC', city_id[0])
        city_name.get_hotel_skyScanner(city_id[1])

main()

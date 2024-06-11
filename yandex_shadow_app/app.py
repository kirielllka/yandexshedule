import requests
import datetime

class Yandex_shadow_app:
    def __init__(self,from_city:str='Moscow',to_city:str='Kazan'):
        self.__api_yandex_key = '38335cf3-404a-41e2-9e73-71b3382508c9'
        self.__api_wmap_key = '0b2956298069401c2f7cc95090daa6ba'
        self.__city_From = from_city
        self.__city_To = to_city
        self.__shadow_between_city_request= 'https://api.rasp.yandex.net/v3.0/'
        self.__geocod_request = f'https://api.openweathermap.org/data/2.5/weather?'
        self.__nearest_city_req = 'https://api.rasp.yandex.net/v3.0/nearest_settlement/?'
        self.last_result = []
    async def get_coord(self):
        request_coords_from = [(requests.get(self.__geocod_request + f'q={self.__city_From}&appid={self.__api_wmap_key}').json())['coord']['lon'],requests.get(self.__geocod_request + f'q={self.__city_From}&appid={self.__api_wmap_key}').json()['coord']['lat']]
        request_coords_to = [(requests.get(self.__geocod_request + f'q={self.__city_To}&appid={self.__api_wmap_key}').json())['coord']['lon'],requests.get(self.__geocod_request + f'q={self.__city_To}&appid={self.__api_wmap_key}').json()['coord']['lat']]
        return {'from':request_coords_from,'to':request_coords_to}

    async def get_city_coord(self,city:str)->list:
        return [(requests.get(self.__geocod_request + f'q={city}&appid={self.__api_wmap_key}').json())['coord']['lon'],requests.get(self.__geocod_request + f'q={self.__city_From}&appid={self.__api_wmap_key}').json()['coord']['lat']]

    async def get_near_station(self, city:str)->dict:
        coords = await self.get_city_coord(city)
        req = requests.get(self.__shadow_between_city_request + 'nearest_stations/' + f'?apikey={self.__api_yandex_key}&lat={coords[1]}&lng={coords[0]}').json()
        print(req)
        return req

    async def get_code_station(self,city,station):
        coords = await self.get_city_coord(city)
        req = requests.get(self.__shadow_between_city_request + 'nearest_stations/' + f'?apikey={self.__api_yandex_key}&lat={coords[1]}&lng={coords[0]}').json()
        code = ''
        for i in req['stations']:
            if i['title'] == station:
                code = i['code']
        return code
    async def all_stationt(self, code:str)->dict:
        request = requests.get(f'{self.__shadow_between_city_request}schedule/?apikey={self.__api_yandex_key}&station={code}').json()
        return request
    async def __get_code(self,get_coords:dict):
        request_city_from_code = requests.get(self.__nearest_city_req + f'apikey={self.__api_yandex_key}&format=json&lat={get_coords['from'][1]}&lng={get_coords['from'][0]}').json()['code']
        request_city_to_code = requests.get(self.__nearest_city_req + f'apikey={self.__api_yandex_key}&format=json&lat={get_coords['from'][1]}&lng={get_coords['to'][0]}').json()['code']
        return [request_city_from_code,request_city_to_code]
    async def get_shadow_between_citis(self,date)->dict:
        if self.last_result == []:
            get_coords = await self.get_coord()
            codes = await self.__get_code(get_coords=get_coords)
            request = self.__shadow_between_city_request+'search/'+f'?apikey={self.__api_yandex_key}&from={codes[0]}&to={codes[1]}&date={date}'
            shadow_request = requests.get(self.__shadow_between_city_request+'search/'+f'?apikey={self.__api_yandex_key}&from={codes[0]}&to={codes[1]}&date={date}').json()
            print(request)
            result = []
            for segment in shadow_request['segments']:
                races_dict = {}
                races_dict['Название'] = str(segment['thread']['title'])
                races_dict['Транспорт'] = str(segment['from']['transport_type'])
                races_dict['Откуда'] = str(segment['from']['title'])
                races_dict['Время отправления'] = str(segment['departure'][11:19])
                races_dict['Куда'] = str(segment['to']['title'])
                races_dict['Время прибытия'] = str(segment['arrival'][11:19])
                if races_dict not in result:
                    result.append(races_dict)
            return result
        else:
            return self.last_result


    @property
    def city_From(self):
        return self.__city_From
    @city_From.setter
    def city_From(self,new_data):
        self.__city_From = new_data
        self.__last_result = []
    @property
    def city_To(self):
        return self.__city_To

    @city_To.setter
    def city_To(self, data):
        self.__city_To = data





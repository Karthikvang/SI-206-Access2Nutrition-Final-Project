import requests
import sqlite3


openweather_key = '6cebbdc5722158ef937fa0f74650b54b'

def get_geocode(city_str):
    limit = 1
    url = f'''http://api.openweathermap.org/geo/1.0/direct?q={city_str},
    US-MI,840&limit={limit}&appid={openweather_key}'''

    geocode = requests.get(url).json()

    latitude = geocode[0]['lat']
    longitude = geocode[0]['lon']

    latitude = round(latitude, 2)
    longitude = round(longitude,2)

    return (latitude, longitude)
    

def get_summer_data (city):
    start = '1687665600'
    end = '1688788800'
    # url = f'''https://history.openweathermap.org/data/2.5/history/city?
    # lat={lat}&lon={lon}&type=hour&start={start}&end={end}&appid={openweather_key}'''
    url = f'''https://history.openweathermap.org/data/2.5/history/city?
    q={city},US-MI&type=hour&start={start}&end={end}&appid={openweather_key}'''
    response = requests.get(url)
    print(response.json())


# def get_winter_data(city_str):
#     pass

def main():

    get_summer_data('Ann Arbor')
    conn = sqlite3.connect('A2N.db')
    cur = conn.cursor()
   

if __name__ == "__main__":
    main()

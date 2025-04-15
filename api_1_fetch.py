import requests
import sqlite3
import datetime


openweather_key = '6cebbdc5722158ef937fa0f74650b54b'
DAY_INCREMENT = 86400

# May 2024
# July 2024
# September 2024
# January 2025

def get_geocode(city_str):
    limit = 1
    url = f'''http://api.openweathermap.org/geo/1.0/direct?q={city_str}, MI, USA&limit={limit}&appid={openweather_key}'''
    geocode = requests.get(url).json()

    latitude = geocode[0]['lat']
    longitude = geocode[0]['lon']

    return (latitude, longitude)


def get_may_data(lat, lon):
    start = 1714536000 # May 1 2024 12:00AM
    end = 1714622400 # May 2 2024 12:00AM

    while int(start) <= int(end):

        # Call data for noon of every day in may
        url = f'https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&appid={openweather_key}&start={str(start)}&end={str(end)}&units=imperial'
        response = requests.get(url)
        response = response.json()['list'][9]

        # Change date from unix timestamp into regular calendar date
        timestamp = response['dt']
        date = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)
        response['dt'] = str(date.date())

        # Move on to the next day
        start += DAY_INCREMENT
        end += DAY_INCREMENT

    return response
    

def create_db():
    conn = sqlite3.connect('A2N.db')
    cur = conn.cursor()

    # City
    # Date
    # Time
    # Temperature

    cur.execute("""CREATE TABLE IF NOT EXISTS weather (
                
                
                )""")


def insert_seasons (season, cur, conn, limit = 25):
    
    for city in season:
        for item in season[city]['list']:
            time = item[city]['dt']
            print(time)
            temp = item['main']['temp']

def main():
    summer_dict = {}
    winter_dict = {}

    # Get geocodes to help API locate city coordinates
    aa_geocode = get_geocode('Ann Arbor')
    dt_geocode = get_geocode('Detroit')
    pc_geocode = get_geocode('Pontiac')

    # Organize returned data into summer & winter dictionaries
    get_may_data(aa_geocode[0], aa_geocode[1])
    
    

    # insert_seasons(summer_dict, cur, conn)

   

if __name__ == "__main__":
    main()

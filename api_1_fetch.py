import requests
import sqlite3


openweather_key = '6cebbdc5722158ef937fa0f74650b54b'

def get_geocode(city_str):
    limit = 1
    url = f'''http://api.openweathermap.org/geo/1.0/direct?q={city_str}, MI, USA&limit={limit}&appid={openweather_key}'''
    geocode = requests.get(url).json()

    latitude = geocode[0]['lat']
    longitude = geocode[0]['lon']

    return (latitude, longitude)
    

def get_summer_data (lat, lon):
    start = '1719720000' # June 30 2024
    end = '1720411200' # July 8 2024
   
    url = f'https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&appid={openweather_key}&start={start}&end={end}&units=imperial'
    response = requests.get(url)

    return response.json()


def get_winter_data(lat, lon):
    start = '1734843600' # December 22 2024
    end = '1735362000' # December 28 2024

    url = f'https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&appid={openweather_key}&start={start}&end={end}&units=imperial'
    response = requests.get(url)

    print(response.json())
    return response.json()

def insert_seasons (season, cur, conn, limit = 25):
    #counter to track how many holidays been inserted
    inserted = 0
    #go thru each holiday in list
    for city in season:
        #stop if my limit (of 25) has been reached
        if inserted >= limit:
            break

        #this gets name and date of holidays
        name = holiday['name']
        date = holiday['date']['iso']

        #check if name and date already in table
        cur.execute('''
                    SELECT id FROM holidays WHERE name = ? AND date = ?
                     ''', (name, date))
        result = cur.fetchone()
    #if there is a match then skip (NO DUPLICATES)
        if result: 
            continue
    #insert new non duplicate holiday into table
        else:
            cur.execute('''
                INSERT INTO holidays (name, date)
                VALUES (?, ?)
            ''', (name, date))
    #if inserted then increment counter
            if cur.rowcount == 1:
                inserted += 1

    conn.commit()
    #small print note i have right now to
    # tell me how many holidays are inserted
    print(f"{inserted} days inserted.")

def main():
    summer_dict = {}
    winter_dict = {}

    # Get geocodes to help API locate city coordinates
    aa_geocode = get_geocode('Ann Arbor')
    dt_geocode = get_geocode('Detroit')
    pc_geocode = get_geocode('Pontiac')

    # Organize returned data into summer & winter dictionaries
    summer_dict['Ann Arbor'] = get_summer_data(aa_geocode[0], aa_geocode[1])
    summer_dict['Detroit'] = get_summer_data(dt_geocode[0], dt_geocode[1])
    summer_dict['Pontiac'] = get_summer_data(pc_geocode[0], pc_geocode[1])

    winter_dict['Ann Arbor'] = get_winter_data(aa_geocode[0], aa_geocode[1])
    winter_dict['Detroit'] = get_winter_data(dt_geocode[0], dt_geocode[1])
    winter_dict['Pontiac'] = get_winter_data(pc_geocode[0], pc_geocode[1])
    
    # conn = sqlite3.connect('A2N.db')
    # cur = conn.cursor()
   

if __name__ == "__main__":
    main()

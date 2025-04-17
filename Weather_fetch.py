import requests
import sqlite3
import datetime


openweather_key = '6cebbdc5722158ef937fa0f74650b54b'
DAY_INCREMENT = 86400 # Number of seconds in a day, required for incrementing days


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

    end_of_month = 1717214400 # June 1 2024

    may_lst = []
    
    while start < end_of_month:

        # Call data for noon of every day in may
        url = f'https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&appid={openweather_key}&start={str(start)}&end={str(end)}&units=imperial'
        response = requests.get(url)
        response = response.json()['list'][12]

        # Change date from unix timestamp into regular calendar date
        timestamp = response['dt']
        date = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)
        response['dt'] = str(date.date())

        # Move on to the next day
        start += DAY_INCREMENT
        end += DAY_INCREMENT

        may_lst.append(response)

    return may_lst


def get_july_data(lat,lon):
    start = 1719806400 # July 1 2024 12:00AM
    end = 1719892800 # July 2 2024 12:00AM

    end_of_month = 1722484800 # August 1 2024

    july_dict = []
    
    while int(start) < end_of_month:

        # Call data for noon of every day in may
        url = f'https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&appid={openweather_key}&start={str(start)}&end={str(end)}&units=imperial'
        response = requests.get(url)
        response = response.json()['list'][12]

        # Change date from unix timestamp into regular calendar date
        timestamp = response['dt']
        date = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)
        response['dt'] = str(date.date())

        # Move on to the next day
        start += DAY_INCREMENT
        end += DAY_INCREMENT

        july_dict.append(response)

    return july_dict
    

def get_september_data(lat,lon):
    start = 1725163200 # September 1 2024 12:00AM
    end = 1725249600 # September 2 2024 12:00AM
    
    end_of_month = 1727755200 # October 1 2024

    september_lst = []

    while int(start) < end_of_month:

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

        september_lst.append(response)


    return september_lst


def get_january_data(lat,lon):
    start = 1735707600 # January 1 2025 12:00AM
    end = 1735794000 # January 2 2025 12:00AM

    end_of_month = 1738386000 # February 1 2025

    january_lst = []
    
    while int(start) < end_of_month:

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
        january_lst.append(response)

    return january_lst

def create_db(cur, conn):
    cur.execute("""CREATE TABLE IF NOT EXISTS city (id INTEGER PRIMARY KEY AUTOINCREMENT, city_name TEXT) """)
    cur.execute("CREATE TABLE IF NOT EXISTS months (id INTEGER PRIMARY KEY AUTOINCREMENT, month TEXT)")
    cur.execute("""CREATE TABLE IF NOT EXISTS temperatures 
                (id INTEGER PRIMARY KEY AUTOINCREMENT, city_id INTEGER, month_id INTEGER, temp INTEGER, 
                FOREIGN KEY(city_id) REFERENCES city(id), FOREIGN KEY(month_id) REFERENCES months(id))""")
    
    conn.commit()


def insert_data (month, city, data, cur, conn, limit = 25):
    inserted = 0
    
    # Load the city name into the database
    cur.execute("""SELECT id FROM city WHERE city_name = ?""", (city,))
    city_res = cur.fetchone()

    if city_res:
        city_res = city_res[0]
    else:
        cur.execute("INSERT INTO city(city_name) VALUES (?)", (city,))
        city_res = cur.lastrowid
        

    # Load the months into the database
    cur.execute("""SELECT id FROM months WHERE month = ? """, (month,))
    month_res = cur.fetchone()

    if month_res:
        month_res = month_res[0]
    else:
        cur.execute("INSERT INTO months (month) VALUES (?)", (month,))
        month_res = cur.lastrowid

    for day in data:
        # Break if the number of loaded statements exceeds 25
        if inserted >= limit:
            break

        date = day['dt']
        temp = day['main']['temp']

        # Load the temperature values into the database
        cur.execute("""INSERT OR IGNORE INTO temperatures (city_id, month_id, temp) 
                    VALUES (?, ?, ?)""",
                    (city_res, month_res, temp))
        
        inserted += 1
        conn.commit()
    
    print(f'{inserted} row(s) inserted') 
    

def main():

    # Get coordinates to help API locate city
    aa_geocode = get_geocode('Ann Arbor')
    dt_geocode = get_geocode('Detroit')
    pc_geocode = get_geocode('Pontiac')
    print("Geocodes created.\n")

    # # Organize returned data into summer & winter dictionaries
    may_data = get_may_data(aa_geocode[0], aa_geocode[1])
    july_data = get_july_data(aa_geocode[0], aa_geocode[1])
    sept_data = get_september_data(aa_geocode[0], aa_geocode[1])
    jan_data = get_january_data(aa_geocode[0], aa_geocode[1])
    print("Ann Arbor API data loaded.\n")

    may_dt = get_may_data(dt_geocode[0], dt_geocode[1])
    jul_dt = get_july_data(dt_geocode[0], dt_geocode[1])
    sept_dt= get_september_data(dt_geocode[0], dt_geocode[1])
    jan_dt = get_january_data(dt_geocode[0], dt_geocode[1])
    print("Detroit API data loaded.\n")

    may_pc = get_may_data(pc_geocode[0], pc_geocode[1])
    jul_pc = get_july_data(pc_geocode[0], pc_geocode[1])
    sept_pc= get_september_data(pc_geocode[0], pc_geocode[1])
    jan_pc = get_january_data(pc_geocode[0], pc_geocode[1])
    print("Pontiac API data loaded.\n")

    conn = sqlite3.connect('A2N.db')
    cur = conn.cursor()
    print("Database connection established.\n")

    create_db(cur, conn)
    print("Database tables created.\n")

    # Ann Arbor
    for i in range(0, len(may_data), 25):
        batch = may_data[i:i+25]
        insert_data('may', 'Ann Arbor', batch, cur, conn)

    for i in range(0, len(july_data), 25):
        batch = july_data[i:i+25]
        insert_data('july', 'Ann Arbor', batch, cur, conn)

    for i in range(0, len(sept_data), 25):
        batch = sept_data[i:i+25]
        insert_data('september', 'Ann Arbor', batch, cur, conn)

    for i in range(0, len(jan_data), 25):
        batch = jan_data[i:i+25]
        insert_data('january', 'Ann Arbor', batch, cur, conn)

    # Detroit
    for i in range(0, len(may_dt), 25):
        batch = may_dt[i:i+25]
        insert_data('may', 'Detroit', batch, cur, conn)
    
    for i in range(0, len(jul_dt), 25):
        batch = jul_dt[i:i+25]
        insert_data('july', 'Detroit', batch, cur, conn)

    for i in range(0, len(sept_dt), 25):
        batch = sept_dt[i:i+25]
        insert_data('september', 'Detroit', batch, cur, conn)
    
    for i in range(0, len(jan_dt), 25):
        batch = jan_dt[i:i+25]
        insert_data('january', 'Detroit', batch, cur, conn)

    # Pontiac
    for i in range(0, len(may_pc), 25):
        batch = may_pc[i:i+25]
        insert_data('may', 'Pontiac', batch, cur, conn)
    
    for i in range(0, len(jul_pc), 25):
        batch = jul_pc[i:i+25]
        insert_data('july', 'Pontiac', batch, cur, conn)
    
    for i in range(0, len(sept_pc), 25):
        batch = sept_pc[i:i+25]
        insert_data('september', 'Pontiac', batch, cur, conn)
    
    for i in range(0, len(jan_pc), 25):
        batch = jan_pc[i:i+25]
        insert_data('january', 'Pontiac', batch, cur, conn)

    print("API data successfully inserted into database.\n")
    


   

if __name__ == "__main__":
    main()

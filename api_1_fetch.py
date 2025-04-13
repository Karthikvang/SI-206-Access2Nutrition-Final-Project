import requests
import sqlite3


weatherstack_key = '42f2c4f28194060340e97220c64eb8af'

def get_summer_data (city_str):

    # Prints the data of whatever city input into the function
    url = f"https://api.weatherstack.com/historical?access_key={weatherstack_key}"
    query = {"query":city_str, "historical_date_start":"2023-06-01", "historical_date_end":"2023-07-31"}
    summer = requests.get(url, params=query)

    return (summer.json())


def get_winter_data(city_str):
    url = f"https://api.weatherstack.com/current?access_key={weatherstack_key}"
    query = {"query":city_str, "historical_date_start":"2023-11-01", "historical_date_end":"2023-12-31"}
    winter = requests.get(url, params=query)

    return (winter.json())

def main():
    summer_info = {}
    winter_info = {}

    winter_info["Ann Arbor"] = get_winter_data('Ann Arbor')
    summer_info["Ann Arbor"] = get_summer_data('Ann Arbor')
    print("Ann Arbor successfully retreived")

    winter_info["Detroit"] = get_winter_data('Detroit')
    summer_info["Detroit"] = get_summer_data('Detroit')
    print("Detroit successfully retreived")

    winter_info["Marquette"] = get_winter_data('Marquette')
    summer_info['Marquette'] = get_summer_data('Marquette')
    print('Marquette Succesfully retreived')

    winter_info["Lansing"] = get_winter_data('Lansing')
    summer_info['Lansing'] = get_summer_data('Lansing')
    print("Lansing successfully retreived")

    winter_info["Traverse City"] = get_winter_data('Traverse City')
    summer_info['Traverse City'] = get_summer_data('Traverse City')
    print("Traverse city successfully retreived")

    winter_info["Grand Rapids"] = get_winter_data('Grand Rapids')
    summer_info['Grand Rapids'] = get_summer_data('Grand Rapids')
    print("Grand Rapids successfully retreived")

    print(f"WINTER:\n{winter_info}")

    print(f'SUMMER\n{summer_info}')

    conn = sqlite3.connect('A2N.db')
    cur = conn.cursor()
    # Create the countries table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS SEASONS (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_code TEXT UNIQUE,
    country_name TEXT)''')

if __name__ == "__main__":
    main()

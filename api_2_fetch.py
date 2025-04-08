#calendarific API stuff
#anna is woking in here
#this lets me use sqlite
import sqlite3
#allow requests
import requests
#utilize time
import time

BASE_URL = 'https://calendarific.com/api/v2'
#API KEY
API_KEY = 'MVRNRBvAvQwPU7gbpLmAoypbfnrw9SeT'
COUNTRY_CODE = 'US'
YEAR = 2023

#create database
conn = sqlite3.connect('calendarific.db')
cur = conn.cursor()


# Create the countries table
cur.execute('''
CREATE TABLE IF NOT EXISTS countries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_code TEXT UNIQUE,
    country_name TEXT
)
''')

# Create the holidays table
cur.execute('''
CREATE TABLE IF NOT EXISTS holidays (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    date TEXT,
    country_id INTEGER,
    UNIQUE(name, date),
    FOREIGN KEY(country_id) REFERENCES countries(id)
)
''')

# Commit changes and close connection
conn.commit()
conn.close()



#i made this function to make request to API to fetch holiday data from my API
#I did this for the US (united states) and chose to look at year 2023

def fetch_us_holidays(api_key, year=YEAR, country_code=COUNTRY_CODE):
#first make parameters for a request
    params = {
        'api_key': api_key,
        'country': country_code,
        'year': year
    }
#include parameters with my BASE url to get stuff that I want
    response = requests.get(BASE_URL, params=params)
#make info a dictionary
    data = response.json()
 # return only the list of holidays from the whole JSON response
    return data['response']['holidays']

#when I do request make sure to add params when calling base 
# url the way the example API is within the documentation


#NEXT FUNC: Checks if the country already exists in the 'countries' table.
#If it doesn’t, it inserts it. Returns the country's ID either way.


#Inserts up to `limit`(25) number of unique holidays into the database.
# It uses the 'INSERT OR IGNORE' statement to prevent duplicates
# based on the UNIQUE constraint on (name, date)



if __name__ == "__main__":
   pass 
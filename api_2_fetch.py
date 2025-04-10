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

# Create the holidays table
cur.execute('''
CREATE TABLE IF NOT EXISTS holidays (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    date TEXT,
    UNIQUE(name, date)
)
''')

# Commit changes and close connection
conn.commit()
conn.close()



#i made this function to make request to API to fetch holiday data from my API
#I did this for the US (united states) and chose to look at year 2023

#note for this function above- when I do request make sure to add params when calling base 
# url the way the example API is within the documentation

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
 # return the list of holidays from the whole JSON response
    return data['response']['holidays']

#my goal is to populate my table and i want to make sure i dont have duplicates 
#need to make sure i limit to 25 each time and 100 overall 
#overall want to populate the DB table i created





#Inserts up to `limit`(25) number of unique holidays into the database.
# It uses the 'INSERT OR IGNORE' statement to prevent duplicates
# based on the UNIQUE constraint on (name, date)


#make dictionary with holiday names as 
if __name__ == "__main__":
   pass 
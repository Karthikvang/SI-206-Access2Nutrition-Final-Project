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
COUNTRY_NAME = 'United States'
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



if __name__ == "__main__":
   pass 
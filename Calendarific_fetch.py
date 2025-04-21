#calendarific API stuff
#anna is woking in here
#this lets me use sqlite
import sqlite3
#allow requests
import requests
#utilize time
import time

BASE_URL = 'https://calendarific.com/api/v2/holidays'
#API KEY
API_KEY = 'MVRNRBvAvQwPU7gbpLmAoypbfnrw9SeT'
COUNTRY_CODE = 'US'
YEAR = 2024

#Set up my database and create my holidays table

def create_database():
    conn = sqlite3.connect('FoodRecall.db')
    cur = conn.cursor()

    # Table for months
    cur.execute('''
            CREATE TABLE IF NOT EXISTS holiday_months (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS holidays (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        month_id INTEGER,
        FOREIGN KEY(month_id) REFERENCES holiday_months(id)
    )
    ''')


    conn.commit()
    conn.close()



#i made this function to make request to API to fetch holiday data from my API
#I did this for the US (united states) and chose to look at year 2023

#note for this function above- when I do request make sure to add params when calling base 
# url the way the example API is within the documentation

def fetch_us_holidays(api_key, year=YEAR, country_code=COUNTRY_CODE):
#make parameters for my request
    params = {
        'api_key': api_key,
        'country': country_code,
        'year': year
    }
#include parameters with my BASE url to get stuff that I want
    response = requests.get(BASE_URL, params=params)
#make info a dictionary
    data = response.json()
 #return the list of holidays from the whole JSON response
    return data['response']['holidays']

#my goal is to populate my table and i want to make sure i dont have duplicates 
#need to make sure i limit to 25 each time and 100 overall 

#this function populates my data into my db

#this just sets the months to my int keys 
def insert_holiday_months(cur, conn, limit = 25):
    months = [
        (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
        (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
        (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
    ]
    inserted = 0

    for month_data in months:
        if inserted >= limit:
            break

        cur.execute("SELECT id FROM holiday_months WHERE id = ?", (month_data[0],))
        result = cur.fetchone()

        if not result:
            cur.execute("INSERT INTO holiday_months (id, name) VALUES (?, ?)", month_data)
            inserted += 1

    conn.commit()
    print(f"{inserted} holiday_month rows inserted.")

def insert_holiday_data(holidays, cur, conn, limit = 25):
    #counter to track how many holidays been inserted
    inserted = 0
    
    #go thru each holiday in list
    for holiday in holidays:
        #stop if my limit (of 25) has been reached
        if inserted >= limit:
            break

        #this gets name and date of holidays
        name = holiday['name']
        date = holiday['date']['iso']
        ##get month as int from the date string (since thats what api originally gives me)
        month = int(date.split("-")[1])


        # Check if this holiday name and month_id combo already exists
        cur.execute("SELECT id FROM holidays WHERE name = ? AND month_id = ?", (name, month))
        result = cur.fetchone()

        if result:
            continue  # If it exists, skip to the next holiday

        # Otherwise, insert the holiday with its name and month_id
        cur.execute("INSERT INTO holidays (name, month_id) VALUES (?, ?)", (name, month))

        if cur.rowcount == 1:
            inserted += 1

    # Commit changes to the database
    conn.commit()

    # Let the user know how many holidays were inserted
    print(f"{inserted} holidays inserted.")



def main():
    #function to create my db
    create_database()

    #connect again to insert data
    conn = sqlite3.connect('FoodRecall.db')
    cur = conn.cursor()

    #get holidays from the API
    holidays = fetch_us_holidays(API_KEY)

    #insert month info
    insert_holiday_months(cur, conn, limit=25)

    #insert up to 25 holidays
    insert_holiday_data(holidays, cur, conn, limit = 25)

    #dont forget to close connection
    conn.close()
    






#Inserts up to `limit`(25) number of unique holidays into the database.
# It uses the 'INSERT OR IGNORE' statement to prevent duplicates
# based on the UNIQUE constraint on (name, date)


#make dictionary with holiday names as 
if __name__ == "__main__":
   main()





   
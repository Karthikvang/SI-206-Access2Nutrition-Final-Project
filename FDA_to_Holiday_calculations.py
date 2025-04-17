#anna is working in here 
import sqlite3

#join the holidays and holiday_months tables
#groups the holidays by month
#and count how many holidays are in each month
def count_holidays_per_month():
    conn = sqlite3.connect('A2N.db')
    cur = conn.cursor() 

    cur.execute(''' 
                SELECT holiday_months.name,
                COUNT(*) 
                FROM holidays
                JOIN holiday_months ON holiday_months.id = holidays.month_id
                GROUP BY month_id
                ;
                ''')
    
    results = cur.fetchall()
    print(f"HERE ARE RESULTS:, {results}")

#loop thru to get all months 
    for month_name, count in results:
        print(f"{month_name}: {count} holidays")
    conn.close()

count_holidays_per_month()

def count_recalls_per_month():
    conn = sqlite3.connect('A2N.db')
    cur = conn.cursor() 

    cur.execute(''' 
                SELECT holiday_months.name,
                COUNT(*) 
                FROM holidays
                JOIN holiday_months ON holiday_months.id = holidays.month_id
                GROUP BY month_id
                ;
                ''')
    
    results = cur.fetchall()
    print(f"HERE ARE RESULTS:, {results}")

#loop thru to get all months 
    for month_name, count in results:
        print(f"{month_name}: {count} holidays")
    conn.close()

count_holidays_per_month()







#anna is working in here 
import sqlite3
import json

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

    conn.close()
    return {month: count for month, count in results}

def count_recalls_per_month():
    conn = sqlite3.connect('A2N.db')
    cur = conn.cursor() 

    cur.execute(''' 
                SELECT holiday_months.name,
                COUNT(*) 
                FROM food_recalls
                JOIN holiday_months ON holiday_months.id = food_recalls.recall_initiation_month
                GROUP BY holiday_months.id
                ;
                ''')
    
    results2 = cur.fetchall()
    conn.close()
    return {month: count for month, count in results2}
    
    

def writer(holidays, recalls):
    data = {
        "holidays": holidays,
        "recalls": recalls
    }

    with open("monthly_data.json", "w") as f:
        #json dump writes to the file
        json.dump(data, f, indent=4)

def main():
    holidays_per_month = count_holidays_per_month()
    recalls_per_month = count_recalls_per_month()

    writer(holidays_per_month, recalls_per_month)


if __name__ == "__main__":
    main()









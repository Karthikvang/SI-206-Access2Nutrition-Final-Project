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
    

#loop thru to get all months 
    for month_name, count in results:
        print(f"{month_name}: {count} holidays")
    conn.close()
    return results

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
    
    

#loop thru to get all months 
    for month_name, count in results2:
        print(f"{month_name}: {count} recalls")
    conn.close()
    return results2

def writer(holidays, recalls):
     with open("monthly_summary.txt", "w") as f:
        f.write("Holidays Per Month:\n")
        for month, count in holidays:
            f.write(f"{month}: {count} holidays\n")

        f.write("\nFood Recalls Per Month:\n")
        for month, count in recalls:
            f.write(f"{month}: {count} recalls\n")




def main():
    holidays_per_month = count_holidays_per_month()
    recalls_per_month = count_recalls_per_month()

    writer(holidays_per_month, recalls_per_month)


if __name__ == "__main__":
    main()









import sqlite3

# For calculating the average temperature for a city for a specific month:
# - Select the city
# - Select the Month
# - get the temps for the whole month
# - get the average (sum of temps / number of days)
conn = sqlite3.connect('A2N.db')
cur = conn.cursor()

def warmest_month_aa():
    aa_monthly_avg = cur.execute("""SELECT months.month, AVG(temperatures.temp) AS avg_temp
                         FROM temperatures JOIN months ON temperatures.month_id = months.id 
                         JOIN city ON temperatures.city_id = city.id
                         WHERE city.city_name = ?
                         GROUP BY months.id""", ('Ann Arbor',))
    print(aa_monthly_avg.fetchall())

def main():
    warmest_month_aa()

if __name__ == "__main__":
    main()
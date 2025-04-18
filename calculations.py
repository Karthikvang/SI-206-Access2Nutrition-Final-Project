import sqlite3
import json

# JOSEPH

def fetch_recalls_by_region_month(db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    cur.execute("""
        SELECT
          CASE
            WHEN state IN ('ME','NH','VT','MA','RI','CT','NY','NJ','PA') THEN 'East'
            WHEN state IN ('OH','MI','IN','IL','WI','MN','IA','MO','ND','SD','NE','KS') THEN 'Midwest'
            WHEN state IN ('DE','MD','DC','VA','WV','NC','SC','GA','FL','KY','TN','MS','AL','OK','TX','AR','LA') THEN 'Central'
            ELSE 'West'
          END AS region,

          CASE recall_initiation_month
            WHEN 12 THEN 'Winter' WHEN 1 THEN 'Winter'  WHEN 2 THEN 'Winter'
            WHEN 3  THEN 'Spring' WHEN 4 THEN 'Spring' WHEN 5 THEN 'Spring'
            WHEN 6  THEN 'Summer' WHEN 7 THEN 'Summer' WHEN 8 THEN 'Summer'
            WHEN 9  THEN 'Fall'   WHEN 10 THEN 'Fall'   WHEN 11 THEN 'Fall'
          END AS season,

          COUNT(*) AS recall_count
        FROM food_recalls
        GROUP BY region, season
        ORDER BY
          region,
          CASE recall_initiation_month
            WHEN 12 THEN 1 WHEN 1 THEN 1 WHEN 2 THEN 1
            WHEN 3  THEN 2 WHEN 4 THEN 2 WHEN 5 THEN 2
            WHEN 6  THEN 3 WHEN 7 THEN 3 WHEN 8 THEN 3
            WHEN 9  THEN 4 WHEN 10 THEN 4 WHEN 11 THEN 4
          END;
    """)
    
    rows = cur.fetchall()
    conn.close()

    recalls = {}
    for region, season, count in rows:
        if region not in recalls:
            recalls[region] = {}
        recalls[region][season] = count

    
    return recalls


    
# KARTHIK

def monthly_averages():
    conn = sqlite3.connect('A2N.db')
    cur = conn.cursor()

    return_dict = {}
    sf_monthly_avg = cur.execute("""SELECT months.month, AVG(temperatures.temp) AS avg_temp
                         FROM temperatures JOIN months ON temperatures.month_id = months.id 
                         JOIN city ON temperatures.city_id = city.id
                         WHERE city.city_name = ?
                         GROUP BY months.id""", ('San Francisco',)).fetchall()
    return_dict['San Francisco'] = sf_monthly_avg

    dt_monthly_avg = cur.execute("""SELECT months.month, AVG(temperatures.temp) AS avg_temp
                         FROM temperatures JOIN months ON temperatures.month_id = months.id 
                         JOIN city ON temperatures.city_id = city.id
                         WHERE city.city_name = ?
                         GROUP BY months.id""", ('Detroit',)).fetchall()
    return_dict['Detroit'] = dt_monthly_avg

    ny_monthly_avg = cur.execute("""SELECT months.month, AVG(temperatures.temp) AS avg_temp
                         FROM temperatures JOIN months ON temperatures.month_id = months.id 
                         JOIN city ON temperatures.city_id = city.id
                         WHERE city.city_name = ?
                         GROUP BY months.id""", ('New York',)).fetchall()
    return_dict['New York'] = ny_monthly_avg

    dl_monthly_avg = cur.execute("""SELECT months.month, AVG(temperatures.temp) AS avg_temp
                         FROM temperatures JOIN months ON temperatures.month_id = months.id 
                         JOIN city ON temperatures.city_id = city.id
                         WHERE city.city_name = ?
                         GROUP BY months.id""", ('Dallas',)).fetchall()
    return_dict['Dallas'] = dl_monthly_avg

    return return_dict

# ANNA

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
    
def write_all_results_to_json(joseph_data, karthik_data, anna_holidays, anna_recalls, filename='final_output.json'):
    all_data = {
        "recalls_by_region_and_season": joseph_data,
        "city_monthly_avg_temperatures": karthik_data,
        "holidays_per_month": anna_holidays,
        "recalls_per_month": anna_recalls
    }
    with open(filename, 'w') as f:
        json.dump(all_data, f, indent=4)
    print(f" All data written to {filename}")
   



def main():
    joseph_data = fetch_recalls_by_region_month('A2N.db')
    karthik_data = monthly_averages()
    anna_holidays = count_holidays_per_month()
    anna_recalls = count_recalls_per_month()

    write_all_results_to_json(joseph_data, karthik_data, anna_holidays, anna_recalls)

if __name__ == "__main__":
    main()
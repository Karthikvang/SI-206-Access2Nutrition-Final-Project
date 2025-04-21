import sqlite3
import json
import matplotlib.pyplot as plt
import numpy as np

conn = sqlite3.connect('A2N.db')
cur = conn.cursor()


def monthly_averages():
    return_dict = {}
    sf_monthly_avg = cur.execute("""SELECT holiday_months.name, AVG(temperatures.temp) AS avg_temp
                         FROM temperatures JOIN holiday_months ON temperatures.month_id = holiday_months.id 
                         JOIN city ON temperatures.city_id = city.id
                         WHERE city.city_name = ?
                         GROUP BY holiday_months.id""", ('San Francisco',)).fetchall()
    return_dict['San Francisco'] = sf_monthly_avg

    dt_monthly_avg = cur.execute("""SELECT holiday_months.name, AVG(temperatures.temp) AS avg_temp
                         FROM temperatures JOIN holiday_months ON temperatures.month_id = holiday_months.id 
                         JOIN city ON temperatures.city_id = city.id
                         WHERE city.city_name = ?
                         GROUP BY holiday_months.id""", ('Detroit',)).fetchall()
    return_dict['Detroit'] = dt_monthly_avg

    ny_monthly_avg = cur.execute("""SELECT holiday_months.name, AVG(temperatures.temp) AS avg_temp
                         FROM temperatures JOIN holiday_months ON temperatures.month_id = holiday_months.id 
                         JOIN city ON temperatures.city_id = city.id
                         WHERE city.city_name = ?
                         GROUP BY holiday_months.id""", ('New York',)).fetchall()
    return_dict['New York'] = ny_monthly_avg

    dl_monthly_avg = cur.execute("""SELECT holiday_months.name, AVG(temperatures.temp) AS avg_temp
                         FROM temperatures JOIN holiday_months ON temperatures.month_id = holiday_months.id 
                         JOIN city ON temperatures.city_id = city.id
                         WHERE city.city_name = ?
                         GROUP BY holiday_months.id""", ('Dallas',)).fetchall()
    return_dict['Dallas'] = dl_monthly_avg

    return return_dict

def write(dict):
    with open("city_avg_temps.json", "w") as f:
        #json dump writes to the file
        json.dump(dict, f, indent=4)

def main():
    dictionary = monthly_averages()
    write(dictionary)

    


if __name__ == "__main__":
    main()
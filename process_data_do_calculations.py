import sqlite3
import matplotlib.pyplot as plt
import numpy as np

conn = sqlite3.connect('A2N.db')
cur = conn.cursor()

def monthly_averages():
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

def main():
    city_data = monthly_averages()

    # Create graph for temperatures across cities
    month_order = ['may', 'july', 'september', 'january']
    cities = list(city_data.keys())

    city_temps = []
    for city in cities:
        # Sort the data to match month_order
        sorted_temps = sorted(city_data[city], key=lambda x: month_order.index(x[0]))
        city_temps.append([temp for _, temp in sorted_temps])

    # Plot settings
    x = np.arange(len(month_order))  # positions for months
    bar_width = 0.2

    plt.figure(figsize=(12, 6))

    # Plot each city’s bars, shifted by bar width
    for i, temps in enumerate(city_temps):
        positions = x + (i - len(cities)/2) * bar_width + bar_width / 2
        plt.bar(positions, temps, width=bar_width, label=cities[i])

    # Label the axes and adjust margins
    plt.xticks(x, month_order)
    plt.ylabel("Average Temperature (°F)")
    plt.xlabel("Month")
    plt.title("Average Monthly Temperatures by City")
    plt.legend(title="City")
    plt.grid(axis='y')
    plt.show()
            



if __name__ == "__main__":
    main()
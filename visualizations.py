import matplotlib
import matplotlib.pyplot as plt
from  process_data_do_calculations import *

def main():
    city_data = monthly_averages()
    
    # Create graph for temperatures across cities
    month_order = ['may', 'july', 'september', 'january']
    cities = list(city_data.keys())

    # Sort the data to match month_order
    city_temps = []
    for city in cities:
        sorted_temps = sorted(city_data[city], key=lambda x: month_order.index(x[0]))
        city_temps.append([temp for _, temp in sorted_temps])

    # Plot settings
    x = np.arange(len(month_order))
    bar_width = 0.2

    # Plot dimensions
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
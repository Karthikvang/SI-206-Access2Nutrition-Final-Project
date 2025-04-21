import matplotlib.pyplot as plt
import numpy as np
from calculations import *

# JOSEPH

def fda_recalls_visualizations():
    data = fetch_recalls_by_region_month('FoodRecall.db')

    seasons = ['Winter', 'Spring', 'Summer', 'Fall']
    regions = ['East', 'Central', 'Midwest', 'West']

    # Color code regions based on vibe
    region_colors = {
        'East': 'gold',
        'Central': 'gray',
        'Midwest': 'darkorange',
        'West': 'royalblue'
    }

    # 2x2 grid, 4 regions
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))
    axs = axs.flatten()

    for i, region in enumerate(regions):
        ax = axs[i]
        # Get recall counts for region, default to 0 if missing
        counts = [data.get(region, {}).get(season, 0) for season in seasons]

        # Bar chart
        ax.bar(seasons, counts, color=region_colors[region])
        ax.set_title(region)
        ax.set_ylim(0, max(counts) + 2)
        ax.set_ylabel("Recalls")

    fig.suptitle("Food Recalls by Season for Each Region", fontsize=14)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()


# KARTHIK
def weather_visualizations():
    city_data = monthly_averages()
    
    # Create graph for temperatures across cities
    month_order = ['May', 'July', 'September', 'January']
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

# ANNA

def calendar_count_visualizations():
        # Load the data from the JSON file
    with open("monthly_data.json", "r") as f:
        data = json.load(f)

    # Separate the data
    holidays = data["holidays"]
    recalls = data["recalls"]

    # Sort by month order (optional, depending on DB order)
    month_order = ["January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"]

    # Sort dictionaries based on month_order
    holidays_sorted = {month: holidays.get(month, 0) for month in month_order}
    recalls_sorted = {month: recalls.get(month, 0) for month in month_order}

    # --- Plot 1: Line Chart for Holidays Per Month ---
    plt.figure(figsize=(10, 5))
    plt.plot(holidays_sorted.keys(), holidays_sorted.values(), marker='o', linestyle='-', color='pink', label='Holidays')
    plt.title("Number of Holidays Per Month")
    plt.xlabel("Month")
    plt.ylabel("Number of Holidays")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.savefig("holidays_line_chart.png")  # Saves the chart as an image
    plt.show()

    # --- Plot 2: Line Chart for Food Recalls Per Month ---
    plt.figure(figsize=(10, 5))
    plt.plot(recalls_sorted.keys(), recalls_sorted.values(), marker='o', linestyle='-', color='purple', label='Food Recalls')
    plt.title("Number of Food Recalls Per Month")
    plt.xlabel("Month")
    plt.ylabel("Number of Recalls")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.savefig("recalls_line_chart.png")  # Saves the chart as an image
    plt.show()

  
def main():
    fda_recalls_visualizations()
    weather_visualizations()
    calendar_count_visualizations()


if __name__ == "__main__":
    main()
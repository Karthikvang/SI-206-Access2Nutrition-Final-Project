import json
import matplotlib.pyplot as plt

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
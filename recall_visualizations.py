import matplotlib.pyplot as plt
import OpenFDA_calculations as calc

data = calc.fetch_recalls_by_region_month('A2N.db')

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

import csv
import numpy as np
import matplotlib.pyplot as plt

# Read data from CSV
csv_path = "iso.csv"
years = []
iso_sizes = []

with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    for row in reader:
        if row and row[0].strip():  # Skip empty lines
            years.append(int(row[0]))
            iso_sizes.append(float(row[1]))

# Convert to numpy arrays
years = np.array(years)
iso_sizes = np.array(iso_sizes)

# Set style consistent with other figures
plt.rcParams.update({
    "font.family": "serif",
    "axes.labelsize": 14,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 12,
})

fig, ax = plt.subplots(figsize=(10, 6))

ax.set_axisbelow(True)
ax.yaxis.grid(True, linestyle="--", linewidth=0.7, alpha=0.25)
ax.xaxis.grid(True, linestyle="--", linewidth=0.7, alpha=0.25)

for sp in ax.spines.values():
    sp.set_color("#D0D0D0")
    sp.set_linewidth(1.0)

# Plot line with markers
line = ax.plot(
    years,
    iso_sizes,
    marker='o',
    markersize=6,
    linewidth=2,
    color="#0080CA",
    markerfacecolor="#0080CA",
    markeredgecolor="white",
    markeredgewidth=1.2,
    zorder=3,
    label="TeX Live ISO Size"
)

# Add value labels on points
for year, size in zip(years, iso_sizes):
    ax.text(
        year,
        size + 0.15,
        f"{size:.1f}",
        ha="center",
        va="bottom",
        fontsize=10,
        color="#333333",
    )

ax.set_xlabel("Year")
ax.set_ylabel("ISO Size (GB)")
# ax.set_title("TeX Live ISO Size Trends (2008-2025)", fontsize=14, fontweight="bold", pad=15)

# Set x-axis ticks to show all years
ax.set_xticks(years)
ax.set_xticklabels([str(y) for y in years], rotation=45, ha="right")

ax.set_ylim(0, 6.5)
ax.set_xlim(2007, 2026)

# Legend
ax.legend(
    loc="upper left",
    frameon=False,
    handlelength=1.8,
)

plt.tight_layout()
plt.savefig("iso_size.pdf", bbox_inches="tight")
plt.savefig("iso_size.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.show()

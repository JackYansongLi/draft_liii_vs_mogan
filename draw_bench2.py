import re
import numpy as np
import matplotlib.pyplot as plt

benchmarks = [
    "Deepseek-v3.2",
    "Claude-Sonnet-4.5",
    "Gemini-3-pro",
    "ChatGPT-5.2",
]

data_path = "writing.txt"

with open(data_path, "r", encoding="utf-8") as f:
    rows = [
        list(map(float, re.split(r"[,\s]+", line.strip())))
        for line in f if line.strip()
    ]

data = np.array(rows, dtype=float)

if data.shape != (2, 4):
    raise ValueError(f"Expect 2 rows x 4 cols, got {data.shape}. Check your data.")

series_names = [
    "LaTeX",
    "Mogan",
]

highlight_names = {
    "Mogan"
}

series_colors = {
    "LaTeX":   "#CFDDC3",
    "Mogan": "#76C63E",
}

plt.rcParams.update({
    "font.family": "serif",
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
})

fig, ax = plt.subplots(figsize=(11, 6))

x = np.arange(len(benchmarks))
n = len(series_names)
bar_w = 0.30
offsets = (np.arange(n) - (n - 1) / 2) * (bar_w + 0.02)

ax.set_axisbelow(True)
ax.yaxis.grid(True, linestyle="--", linewidth=0.7, alpha=0.25)

for sp in ax.spines.values():
    sp.set_color("#D0D0D0")
    sp.set_linewidth(1.0)

for i, name in enumerate(series_names):
    vals = data[i]
    bars = ax.bar(
        x + offsets[i],
        vals,
        width=bar_w,
        label=name,
        color=series_colors[name],
        edgecolor="white",
        linewidth=0.8,
        zorder=3,
    )

    for b, v in zip(bars, vals):
        ax.text(
            b.get_x() + b.get_width() / 2,
            b.get_height(),
            f"{int(v)}",
            ha="center",
            va="bottom",
            fontsize=12,
            fontweight="bold" if name in highlight_names else "normal",
        )

ax.set_xticks(x)
ax.set_xticklabels(benchmarks, ha="center")
ax.tick_params(axis="x", pad=10)

ax.set_ylabel("Total   Utility")
ax.set_ylim(0, 105)

ax.legend(
    ncol=2,
    loc="upper left",
    bbox_to_anchor=(0.01, 1.02),
    frameon=False,
    handlelength=1.8,
    columnspacing=1.5,
)

plt.tight_layout(rect=[0.00, 0.00, 1.00, 1.00])
plt.savefig("writing.pdf", bbox_inches="tight")
plt.savefig("writing.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.show()

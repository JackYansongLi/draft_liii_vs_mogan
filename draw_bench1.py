import re
import numpy as np
import matplotlib.pyplot as plt
import textwrap

benchmarks = [
    "arXiv:1706.03762",
    "arXiv:1405.4980",
    "arXiv:1204.5721",
    "arXiv:2312.10283",
    "arXiv:2405.19674",
    "arXiv:2502.17655",
]

data_path = "full-compile.txt"

with open(data_path, "r", encoding="utf-8") as f:
    rows = [
        list(map(float, re.split(r"[,\s]+", line.strip())))
        for line in f if line.strip()
    ]

data = np.array(rows, dtype=float)

if data.shape != (4, 6):
    raise ValueError(f"Expect 4 rows x 6 cols, got {data.shape}. Check your data file.")

series_names = [
    "LaTeX on Windows",
    "LaTeX on Linux",
    "MoganSTEM on Windows",
    "MoganSTEM on Linux",
]

highlight_names = {
    "MoganSTEM on Windows",
    "MoganSTEM on Linux"
}

series_colors = {
    "LaTeX on Windows":   "#9A4300",
    "LaTeX on Linux":     "#AA7400",
    "MoganSTEM on Windows": "#00BC80",
    "MoganSTEM on Linux":   "#0080CA",
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
bar_w = 0.18
offsets = (np.arange(n) - (n - 1) / 2) * (bar_w + 0.02)

ax.set_axisbelow(True)
ax.yaxis.grid(True, linestyle="--", linewidth=0.7, alpha=0.25)

for sp in ax.spines.values():
    sp.set_color("#D0D0D0")
    sp.set_linewidth(1.0)

# 画柱子
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
            b.get_height() + 1,
            f"{int(v)}",
            ha="center",
            va="bottom",
            fontsize=8,
            fontweight="bold" if name in highlight_names else "normal",
        )

ax.set_xticks(x)
ax.set_xticklabels(benchmarks, rotation=-35, ha="left", rotation_mode="anchor")
# ax.set_xticklabels(benchmarks, ha="center")
ax.tick_params(axis="x", pad=6)

ax.set_ylabel("Time (ms)")
ax.set_ylim(0, 21500)

# Legend across the top (single row)
ax.legend(
    ncol=4,
    loc="upper left",
    bbox_to_anchor=(0.01, 1.02),
    frameon=False,
    handlelength=1.8,
    columnspacing=1.5,
)

plt.tight_layout(rect=[0.00, 0.00, 1.00, 1.00])
plt.show()

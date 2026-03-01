import re
import numpy as np
import matplotlib.pyplot as plt

benchmarks = [
    "arXiv:1706.03762",
    "arXiv:1405.4980",
    "arXiv:1204.5721",
    "arXiv:2312.10283",
    "arXiv:2405.19674",
    "arXiv:2502.17655",
]

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

# -----------------------------
# Colorblind-safe palette
# -----------------------------
series_colors = {
    "LaTeX on Windows":      "#D55E00",  # Vermillion
    "LaTeX on Linux":        "#D55E00",
    "MoganSTEM on Windows":  "#0072B2",  # Blue
    "MoganSTEM on Linux":    "#0072B2",
}

series_hatch = {
    "LaTeX on Windows":      "",
    "LaTeX on Linux":        "\\\\\\",
    "MoganSTEM on Windows":  "",
    "MoganSTEM on Linux":    "///",
}

charts = [
    {"name": "full-compile", "data_path": "full-compile.txt", "ylim": (0, 21500)},
    {"name": "inc-update", "data_path": "inc-update.txt", "ylim": (0, 12000)},
]

plt.rcParams.update({
    "font.family": "serif",
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "hatch.color": "black",
    "hatch.linewidth": 0.8,
})

bar_w = 0.18
label_fontsize = 8
offsets = (np.arange(len(series_names)) - (len(series_names) - 1) / 2) * (bar_w + 0.02)

for cfg in charts:
    with open(cfg["data_path"], "r", encoding="utf-8") as f:
        rows = [
            list(map(float, re.split(r"[,\s]+", line.strip())))
            for line in f if line.strip()
        ]

    data = np.array(rows, dtype=float)

    if data.shape != (4, 6):
        raise ValueError(f"Expect 4 rows x 6 cols, got {data.shape}. Check your data file.")

    fig, ax = plt.subplots(figsize=(11, 6))
    x = np.arange(len(benchmarks))

    # Grid
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, linestyle="--", linewidth=0.6, alpha=0.25)

    # Subtle axis frame
    for sp in ax.spines.values():
        sp.set_color("#C8C8C8")
        sp.set_linewidth(0.8)

    # Dynamic label offset (1% of y-range)
    y_range = cfg["ylim"][1] - cfg["ylim"][0]
    label_offset = y_range * 0.01

    # Plot bars
    for i, name in enumerate(series_names):
        vals = data[i]

        bars = ax.bar(
            x + offsets[i],
            vals,
            width=bar_w,
            label=name,
            color=series_colors[name],
            hatch=series_hatch[name],
            zorder=3,
        )

        # 对每个 patch 设置：先画填充，再单独画 hatch 线条
        for patch in bars:
            patch.set_hatch(series_hatch[name])
            patch.set_edgecolor("black")  # hatch 线条颜色
            patch.set_linewidth(0)  # 隐藏边框，只保留 hatch
            # 关键：关闭填充，用双层绘制（底层填充 + 上层 hatch）
            # 或用 zorder 确保 hatch 在上
            patch.set_zorder(2)

        # Value labels
        for b, v in zip(bars, vals):
            ax.text(
                b.get_x() + b.get_width() / 2,
                b.get_height() + label_offset,
                f"{int(v)}",
                ha="center",
                va="bottom",
                fontsize=label_fontsize,
                fontweight="bold" if name in highlight_names else "normal",
            )

    # Axes
    ax.set_xticks(x)
    ax.set_xticklabels(benchmarks, rotation=-35, ha="left", rotation_mode="anchor")
    ax.tick_params(axis="x", pad=6)

    ax.set_ylabel("Time (ms)")
    ax.set_ylim(*cfg["ylim"])

    # Legend
    ax.legend(
        ncol=4,
        loc="upper left",
        bbox_to_anchor=(0.01, 1.02),
        frameon=False,
        handlelength=2.5,
        columnspacing=1.5,
        handletextpad=0.3,
    )

    plt.tight_layout()
    plt.savefig(f"{cfg['name']}.pdf", bbox_inches="tight")
    plt.savefig(f"{cfg['name']}.png", dpi=300, bbox_inches="tight", facecolor="white")
    plt.show()


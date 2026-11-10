"""
Generate the result figures shown in README.md from the CSV files in results/.

    python plot_results.py

Each figure is written twice to figures/: <name>.png (light) and <name>_dark.png.
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import LinearSegmentedColormap, Normalize, to_rgb
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter, MultipleLocator
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"

RUNS = ["Run 1", "Run 2 (focus_53)"]

# Figures are laid out at 100 px/inch and saved at 2x, so an 8.5 in wide figure
# lands at the width of a GitHub README column with text at its intended size.
WIDTH = 8.5
DPI = 200
LW = 1.5        # ~2 px line
MS = 7          # ~9 px marker
RING = 1.5      # ~2 px surface ring around markers / gap between heatmap cells

THEMES = {
    "light": dict(
        surface="#fcfcfb", ink="#0b0b0b", ink2="#52514e", muted="#898781",
        grid="#e1e0d9", axis="#c3c2b7",
        runs=["#2a78d6", "#eb6834"],
        diverging=["#184f95", "#3987e5", "#b7d3f6", "#f0efec", "#f5b8b7", "#e34948", "#a12a2a"],
    ),
    "dark": dict(
        surface="#1a1a19", ink="#f0efec", ink2="#c3c2b7", muted="#898781",
        grid="#2c2c2a", axis="#383835",
        runs=["#3987e5", "#d95926"],
        diverging=["#9ec5f4", "#3987e5", "#1c4f8a", "#383835", "#8a2e2e", "#e66767", "#f4a5a5"],
    ),
}

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Segoe UI", "Helvetica Neue", "Arial", "DejaVu Sans"],
    "axes.unicode_minus": True,
})


# ============================================================
# SHARED STYLING
# ============================================================

def new_figure(t, height, title, subtitle):

    fig = plt.figure(figsize=(WIDTH, height), facecolor=t["surface"])

    x = 0.22 / WIDTH
    fig.text(x, 1 - 0.18 / height, title, fontsize=13, fontweight="semibold",
             color=t["ink"], va="top")
    fig.text(x, 1 - 0.46 / height, subtitle, fontsize=9.5, color=t["ink2"], va="top")

    return fig


def style_axes(ax, t, ygrid=True):

    ax.set_facecolor(t["surface"])

    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(t["axis"])
    ax.spines["bottom"].set_linewidth(0.75)

    ax.tick_params(colors=t["ink2"], labelsize=9, length=0, pad=6)
    ax.xaxis.label.set_color(t["ink2"])
    ax.yaxis.label.set_color(t["ink2"])

    if ygrid:
        ax.grid(axis="y", color=t["grid"], linewidth=0.75)
        ax.set_axisbelow(True)


def distance_axis(ax):

    ax.set_xlim(30, 80)
    ax.xaxis.set_major_locator(MultipleLocator(10))
    ax.set_xlabel("Camera distance (cm)", fontsize=9)


def run_legend(fig, t, height, labels, extra=()):

    handles = [
        Line2D([], [], color=c, lw=LW, marker="o", ms=MS, mec=t["surface"], mew=RING)
        for c in t["runs"]
    ]
    leg = fig.legend(
        handles + [h for h, _ in extra], labels + [l for _, l in extra],
        loc="upper left", bbox_to_anchor=(0.16 / WIDTH, 1 - 0.72 / height),
        ncol=len(labels) + len(extra), frameon=False, fontsize=9,
        handlelength=2.2, columnspacing=1.8,
    )
    for text in leg.get_texts():
        text.set_color(t["ink"])


def plot_run(ax, t, color, x, y):

    ax.plot(x, y, color=color, lw=LW, marker="o", ms=MS, mec=t["surface"], mew=RING,
            solid_capstyle="round", solid_joinstyle="round", zorder=3)


def save(fig, name, theme):

    suffix = "" if theme == "light" else "_dark"
    fig.savefig(FIGURES / f"{name}{suffix}.png", dpi=DPI, facecolor=fig.get_facecolor())
    plt.close(fig)


# ============================================================
# FIGURE 1: STEP-HEIGHT RMSE VS DISTANCE
# ============================================================

def plot_rmse(t, theme):

    df = pd.read_csv(RESULTS / "plane_to_plane_rmse.csv")

    height = 4.4
    fig = new_figure(
        t, height, "Step-height RMSE vs camera distance",
        "RMSE of the four measured step heights against ground truth (1, 2, 4, 8 mm). Lower is better.",
    )
    fig.subplots_adjust(left=0.09, right=0.95, top=1 - 1.25 / height, bottom=0.14)
    ax = fig.add_subplot()
    style_axes(ax, t)
    distance_axis(ax)

    labels = []
    for run, color in zip(RUNS, t["runs"]):
        d = df[df.run == run].sort_values("distance_cm")
        plot_run(ax, t, color, d.distance_cm, d.reported_rmse_mm)

        best = d.loc[d.reported_rmse_mm.idxmin()]
        labels.append(f"{run}  ·  best {best.reported_rmse_mm:.3f} mm at {best.distance_cm:.0f} cm")

        last = d.iloc[-1]
        ax.annotate(run.split(" (")[0], (last.distance_cm, last.reported_rmse_mm),
                    xytext=(9, 0), textcoords="offset points", va="center",
                    fontsize=9, color=t["ink"])

    ax.axvline(53, color=t["axis"], lw=0.75, zorder=1)
    ax.text(53, 0.355, "  53 cm", fontsize=9, color=t["ink2"], va="top")

    ax.set_ylim(0, 0.36)
    ax.yaxis.set_major_locator(MultipleLocator(0.05))
    ax.set_ylabel("RMSE (mm)", fontsize=9)

    run_legend(fig, t, height, labels)
    save(fig, "step_height_rmse", theme)


# ============================================================
# FIGURE 2: SIGNED STEP-HEIGHT ERROR HEATMAP
# ============================================================

def ink_on(rgb):

    r, g, b = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb[:3]]
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b

    return "#0b0b0b" if luminance > 0.3 else "#ffffff"


def plot_step_error(t, theme):

    df = pd.read_csv(RESULTS / "plane_to_plane.csv")
    df["error_mm"] = df.measured_mm - df.gt_mm

    cmap = LinearSegmentedColormap.from_list("error", t["diverging"])
    norm = Normalize(-0.6, 0.6)

    height = 4.0
    fig = new_figure(
        t, height, "Step-height error by camera distance",
        "Measured minus ground truth (mm), matched by true step height. "
        "Blue = underestimated, red = overestimated.",
    )
    widths = [df[df.run == run].distance_cm.nunique() for run in RUNS]
    gs = fig.add_gridspec(1, 3, width_ratios=[*widths, 0.22], wspace=0.08,
                          left=0.115, right=0.92, top=1 - 1.15 / height, bottom=0.11)

    for i, run in enumerate(RUNS):
        ax = fig.add_subplot(gs[i])
        style_axes(ax, t, ygrid=False)
        ax.spines["bottom"].set_visible(False)

        grid = df[df.run == run].pivot(index="gt_mm", columns="distance_cm", values="error_mm")
        ax.pcolormesh(grid.values, cmap=cmap, norm=norm, edgecolors=t["surface"], linewidth=RING)

        for (r, c), v in np.ndenumerate(grid.values):
            ax.text(c + 0.5, r + 0.5, f"{v:+.3f}".replace("-", "−"), ha="center", va="center",
                    fontsize=8.5, color=ink_on(cmap(norm(v))))

        ax.set_xticks(np.arange(grid.shape[1]) + 0.5, [f"{d} cm" for d in grid.columns])
        ax.set_yticks(np.arange(grid.shape[0]) + 0.5,
                      [f"{g:g} mm step" for g in grid.index] if i == 0 else [])
        ax.set_title(run, loc="left", fontsize=10, color=t["ink"], pad=8)

    cax = fig.add_subplot(gs[2])
    cbar = fig.colorbar(ScalarMappable(norm, cmap), cax=cax, ticks=[-0.6, -0.3, 0, 0.3, 0.6])
    cbar.outline.set_visible(False)
    cbar.ax.tick_params(colors=t["ink2"], labelsize=8.5, length=0)
    cbar.ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:+.1f}".replace("-", "−") if v else "0"))

    save(fig, "step_height_error", theme)


# ============================================================
# FIGURE 3: POINT-TO-PLANE MAE AND STD
# ============================================================

def single_step_handle(t):

    return Line2D([], [], lw=0, marker="o", ms=4.5, color=t["muted"], alpha=0.6), "single step"


def plot_point_to_plane(t, theme):

    df = pd.read_csv(RESULTS / "point_to_plane.csv")

    height = 4.5
    fig = new_figure(
        t, height, "Point-to-plane residuals vs camera distance",
        "Line = mean over the five stair planes; dots = individual planes. Lower is better.",
    )
    fig.subplots_adjust(left=0.08, right=0.98, top=1 - 1.5 / height, bottom=0.13, wspace=0.12)
    axes = fig.subplots(1, 2, sharey=True)

    for ax, metric, name in zip(axes, ["mae_mm", "std_mm"], ["MAE", "STD"]):
        style_axes(ax, t)
        distance_axis(ax)

        for run, color in zip(RUNS, t["runs"]):
            d = df[df.run == run]
            ax.scatter(d.distance_cm, d[metric], s=16, color=color, alpha=0.35, lw=0, zorder=2)
            mean = d.groupby("distance_cm")[metric].mean()
            plot_run(ax, t, color, mean.index, mean.values)

        ax.set_title(f"{name} (mm)", loc="left", fontsize=10, color=t["ink"], pad=8)

    axes[0].set_ylim(0, 0.5)
    axes[0].yaxis.set_major_locator(MultipleLocator(0.1))

    run_legend(fig, t, height, RUNS, extra=[single_step_handle(t)])
    save(fig, "point_to_plane", theme)


# ============================================================
# FIGURE 4: POINTS PER FITTED PLANE
# ============================================================

def plot_points(t, theme):

    df = pd.read_csv(RESULTS / "point_to_plane.csv")

    height = 3.9
    fig = new_figure(
        t, height, "Points per fitted plane",
        "Valid 3D points inside each stair ROI. Line = mean over the five planes; dots = individual planes.",
    )
    fig.subplots_adjust(left=0.08, right=0.97, top=1 - 1.25 / height, bottom=0.15)
    ax = fig.add_subplot()
    style_axes(ax, t)
    distance_axis(ax)

    for run, color in zip(RUNS, t["runs"]):
        d = df[df.run == run]
        ax.scatter(d.distance_cm, d.n_points, s=16, color=color, alpha=0.35, lw=0, zorder=2)
        mean = d.groupby("distance_cm").n_points.mean()
        plot_run(ax, t, color, mean.index, mean.values)

    ax.set_ylim(0, 800_000)
    ax.yaxis.set_major_locator(MultipleLocator(200_000))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v / 1000:.0f}K" if v else "0"))

    run_legend(fig, t, height, RUNS, extra=[single_step_handle(t)])
    save(fig, "points_per_plane", theme)


# ============================================================
# DATA CHECKS
# ============================================================

def check_reported_rmse():

    steps = pd.read_csv(RESULTS / "plane_to_plane.csv")
    reported = pd.read_csv(RESULTS / "plane_to_plane_rmse.csv")

    steps["sq_err"] = (steps.measured_mm - steps.gt_mm) ** 2
    rmse = np.sqrt(steps.groupby(["run", "distance_cm"]).sq_err.mean()).rename("rmse_mm")

    merged = reported.join(rmse, on=["run", "distance_cm"])
    for _, row in merged[(merged.reported_rmse_mm - merged.rmse_mm).abs() > 0.001].iterrows():
        print(f"WARNING: {row.run} @ {row.distance_cm} cm: reported RMSE {row.reported_rmse_mm:.4f} mm, "
              f"but the step heights give {row.rmse_mm:.4f} mm")


# ============================================================
# RUN
# ============================================================

def main():

    FIGURES.mkdir(exist_ok=True)
    check_reported_rmse()

    for theme, t in THEMES.items():
        plot_rmse(t, theme)
        plot_step_error(t, theme)
        plot_point_to_plane(t, theme)
        plot_points(t, theme)

    print("Figures written to", FIGURES)


if __name__ == "__main__":
    main()

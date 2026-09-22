"""
visualizer.py
--------------
Generates the chart set for the EV Charge & Range Analysis tool and
saves them as PNG files in output/. Uses matplotlib only, so it runs
anywhere pandas + matplotlib are installed (no browser/JS required).
"""

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

from . import analysis

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"

plt.style.use("seaborn-v0_8-darkgrid")
COLORS = ["#3B82F6", "#22C55E", "#F97316", "#A855F7", "#EF4444"]


def _save(fig, name: str):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / name
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {path}")


def plot_range_accuracy(df: pd.DataFrame):
    table = analysis.range_accuracy_by_model(df)
    fig, ax = plt.subplots(figsize=(8, 5))
    x = range(len(table))
    ax.bar(x, table["avg_estimated_range_km"], width=0.35, label="Estimated range", color=COLORS[0])
    ax.bar([i + 0.35 for i in x], table["avg_actual_range_km"], width=0.35, label="Actual range", color=COLORS[1])
    ax.set_xticks([i + 0.175 for i in x])
    ax.set_xticklabels(table.index, rotation=20, ha="right")
    ax.set_ylabel("Range (km)")
    ax.set_title("Estimated vs. Actual Range by Vehicle Model")
    ax.legend()
    _save(fig, "range_accuracy_by_model.png")


def plot_charging_speed(df: pd.DataFrame):
    table = analysis.charging_speed_by_charger_type(df)
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar(table.index, table["avg_charge_speed_km_per_hr"], color=COLORS[:len(table)])
    ax.set_ylabel("Avg. range added per hour (km/hr)")
    ax.set_title("Charging Speed by Charger Type")
    _save(fig, "charging_speed_by_charger_type.png")


def plot_temperature_impact(df: pd.DataFrame):
    table = analysis.temperature_impact(df)
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(table.index.astype(str), table["avg_range_gap_pct"], marker="o", color=COLORS[3], linewidth=2)
    ax.set_ylabel("Avg. range gap (%)")
    ax.set_title("Ambient Temperature vs. Range Prediction Gap")
    ax.tick_params(axis="x", rotation=15)
    _save(fig, "temperature_impact.png")


def plot_battery_degradation(df: pd.DataFrame):
    table = analysis.battery_degradation_trend(df)
    fig, ax1 = plt.subplots(figsize=(8, 5))
    ax1.plot(table.index, table["avg_degradation_pct"], color=COLORS[4], label="Degradation %")
    ax1.set_xlabel("Battery age (months)")
    ax1.set_ylabel("Degradation (%)", color=COLORS[4])

    ax2 = ax1.twinx()
    ax2.plot(table.index, table["avg_actual_range_km"], color=COLORS[0], label="Actual range (km)")
    ax2.set_ylabel("Actual range (km)", color=COLORS[0])

    ax1.set_title("Battery Degradation and Range vs. Battery Age")
    _save(fig, "battery_degradation_trend.png")


def plot_driving_style(df: pd.DataFrame):
    table = analysis.driving_style_summary(df)
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.bar(table.index, table["avg_actual_range_km"], color=COLORS[:len(table)])
    ax.set_ylabel("Avg. actual range (km)")
    ax.set_title("Driving Style vs. Achieved Range")
    _save(fig, "driving_style_vs_range.png")


def generate_all_charts(df: pd.DataFrame):
    plot_range_accuracy(df)
    plot_charging_speed(df)
    plot_temperature_impact(df)
    plot_battery_degradation(df)
    plot_driving_style(df)

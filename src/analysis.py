"""
analysis.py
------------
Summary statistics and aggregations used by the visualizer and the
CLI report. Kept separate from plotting so the numbers can also be
reused for tests or a future API.
"""

import pandas as pd


def range_accuracy_by_model(df: pd.DataFrame) -> pd.DataFrame:
    """How close estimated range is to real-world driven range, per model."""
    return (
        df.groupby("vehicle_model")
        .agg(
            avg_estimated_range_km=("estimated_range_km", "mean"),
            avg_actual_range_km=("actual_range_km", "mean"),
            avg_range_gap_pct=("range_gap_pct", "mean"),
            sessions=("session_id", "count"),
        )
        .round(1)
        .sort_values("avg_range_gap_pct", ascending=False)
    )


def charging_speed_by_charger_type(df: pd.DataFrame) -> pd.DataFrame:
    """Average effective range added per hour, by charger type."""
    return (
        df.groupby("charger_type")
        .agg(
            avg_charge_duration_hrs=("charge_duration_hrs", "mean"),
            avg_energy_added_kwh=("energy_added_kwh", "mean"),
            avg_charge_speed_km_per_hr=("charge_speed_km_per_hr", "mean"),
        )
        .round(2)
        .sort_values("avg_charge_speed_km_per_hr", ascending=False)
    )


def temperature_impact(df: pd.DataFrame, bins=(0, 15, 25, 32, 45)) -> pd.DataFrame:
    """Bucket sessions by ambient temperature and compare range gap."""
    labels = ["Cold (<15C)", "Mild (15-25C)", "Warm (25-32C)", "Hot (>32C)"]
    temp_bucket = pd.cut(df["ambient_temp_c"], bins=bins, labels=labels)
    return (
        df.groupby(temp_bucket, observed=True)
        .agg(
            avg_range_gap_pct=("range_gap_pct", "mean"),
            avg_actual_range_km=("actual_range_km", "mean"),
            sessions=("session_id", "count"),
        )
        .round(1)
    )


def battery_degradation_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Relationship between battery age and both degradation and achieved range."""
    return (
        df.groupby("battery_age_months")
        .agg(
            avg_degradation_pct=("battery_degradation_pct", "mean"),
            avg_actual_range_km=("actual_range_km", "mean"),
        )
        .round(2)
        .sort_index()
    )


def driving_style_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("driving_style")
        .agg(
            avg_actual_range_km=("actual_range_km", "mean"),
            avg_range_gap_pct=("range_gap_pct", "mean"),
            sessions=("session_id", "count"),
        )
        .round(1)
    )


def print_report(df: pd.DataFrame) -> None:
    """Console-friendly summary, used by main.py."""
    sections = [
        ("Range accuracy by vehicle model", range_accuracy_by_model(df)),
        ("Charging speed by charger type", charging_speed_by_charger_type(df)),
        ("Impact of ambient temperature on range", temperature_impact(df)),
        ("Driving style vs. achieved range", driving_style_summary(df)),
    ]
    for title, table in sections:
        print(f"\n=== {title} ===")
        print(table)

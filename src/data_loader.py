"""
data_loader.py
---------------
Loads and lightly validates the EV charging/range dataset into a
pandas DataFrame, ready for analysis and visualization.
"""

from pathlib import Path
import pandas as pd

DEFAULT_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "sample_ev_data.csv"


def load_data(path: Path = DEFAULT_DATA_PATH) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"No dataset found at {path}.\n"
            "Generate one with: python -m src.generate_sample_data"
        )

    df = pd.read_csv(path, parse_dates=["session_start"])

    # Basic cleaning / derived columns used throughout the app
    df = df.dropna()
    df["range_gap_km"] = df["estimated_range_km"] - df["actual_range_km"]
    df["range_gap_pct"] = (df["range_gap_km"] / df["estimated_range_km"]) * 100
    df["charge_speed_km_per_hr"] = df["actual_range_km"] / df["charge_duration_hrs"]

    return df


if __name__ == "__main__":
    frame = load_data()
    print(frame.head())
    print(f"\nLoaded {len(frame)} rows, {frame['vehicle_model'].nunique()} vehicle models.")

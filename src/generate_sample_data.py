"""
generate_sample_data.py
------------------------
Creates a synthetic but realistic dataset of EV charging and range
sessions, so the analyzer has something to work with out of the box.

Run directly to (re)generate data/sample_ev_data.csv:
    python -m src.generate_sample_data
"""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

MODELS = [
    ("Tata Nexon EV", 40.5, 312),
    ("MG ZS EV", 50.3, 461),
    ("Hyundai Kona Electric", 39.2, 452),
    ("Tesla Model 3", 57.5, 513),
    ("BYD Atto 3", 60.5, 521),
]

CHARGER_TYPES = ["Level 1 (Home)", "Level 2 (AC Public)", "DC Fast Charger"]
CHARGER_KW = {"Level 1 (Home)": 2.3, "Level 2 (AC Public)": 7.4, "DC Fast Charger": 50.0}

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "sample_ev_data.csv"


def simulate_session(session_id: int, start: datetime):
    model, battery_kwh, rated_range_km = random.choice(MODELS)
    charger = random.choice(CHARGER_TYPES)
    charger_kw = CHARGER_KW[charger]

    start_soc = round(random.uniform(10, 45), 1)        # % battery at plug-in
    target_soc = round(random.uniform(75, 100), 1)       # % battery at unplug
    delta_soc = max(target_soc - start_soc, 1)

    energy_added_kwh = round(battery_kwh * (delta_soc / 100), 2)
    charge_hours = round(energy_added_kwh / charger_kw, 2)

    # Ambient temperature affects real-world efficiency (kWh/km)
    ambient_c = round(random.uniform(5, 42), 1)
    temp_penalty = 0.0
    if ambient_c < 15:
        temp_penalty = (15 - ambient_c) * 0.004
    elif ambient_c > 32:
        temp_penalty = (ambient_c - 32) * 0.003

    base_efficiency = battery_kwh / rated_range_km       # kWh per km, ideal
    real_efficiency = base_efficiency * (1 + temp_penalty + random.uniform(-0.03, 0.03))

    estimated_range_km = round((battery_kwh * (target_soc / 100)) / real_efficiency, 1)
    driving_style = random.choice(["Eco", "Normal", "Aggressive"])
    style_factor = {"Eco": 1.07, "Normal": 1.0, "Aggressive": 0.88}[driving_style]
    actual_range_km = round(estimated_range_km * style_factor, 1)

    battery_age_months = random.randint(1, 48)
    degradation_pct = round(min(battery_age_months * 0.15, 18), 2)

    return {
        "session_id": session_id,
        "vehicle_model": model,
        "battery_capacity_kwh": battery_kwh,
        "rated_range_km": rated_range_km,
        "battery_age_months": battery_age_months,
        "battery_degradation_pct": degradation_pct,
        "charger_type": charger,
        "charger_power_kw": charger_kw,
        "session_start": start.isoformat(timespec="minutes"),
        "start_soc_pct": start_soc,
        "target_soc_pct": target_soc,
        "energy_added_kwh": energy_added_kwh,
        "charge_duration_hrs": charge_hours,
        "ambient_temp_c": ambient_c,
        "driving_style": driving_style,
        "estimated_range_km": estimated_range_km,
        "actual_range_km": actual_range_km,
    }


def generate(n_sessions: int = 500) -> None:
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    start_time = datetime(2026, 1, 1, 6, 0)

    rows = []
    for i in range(1, n_sessions + 1):
        start_time += timedelta(hours=random.uniform(1, 9))
        rows.append(simulate_session(i, start_time))

    with open(DATA_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {n_sessions} charging sessions -> {DATA_PATH}")


if __name__ == "__main__":
    generate()

# EV Charge & Range Analysis Tool ⚡🔋

A Python data-visualization tool for analyzing **electric vehicle charging
behavior** and **real-world range performance**. It answers the questions
every EV owner and analyst actually cares about:

- How does the manufacturer's *estimated* range compare to what drivers
  *actually* get?
- Which charger type (home, public AC, DC fast) charges the fastest per hour?
- How much does ambient temperature eat into your range?
- How fast does battery capacity degrade as a pack ages?
- How much does driving style (eco / normal / aggressive) change range?

## Overview

Electric vehicles combine electrical storage and propulsion systems with
sensors, controls, and software into one connected transportation platform.
This project focuses on the data-analytics layer of that stack: turning raw
charging-session data into clear, decision-useful charts.

## Project structure

```
ev-charge-range-analyzer/
├── main.py                    # CLI entry point (menu-driven)
├── requirements.txt
├── data/
│   └── sample_ev_data.csv     # synthetic sample dataset (auto-generated)
├── output/                    # generated chart PNGs land here
└── src/
    ├── generate_sample_data.py  # builds a realistic synthetic dataset
    ├── data_loader.py           # loads + cleans the dataset into a DataFrame
    ├── analysis.py               # summary stats / aggregations
    └── visualizer.py              # matplotlib chart generation
```

## Getting started

```bash
git clone https://github.com/<your-username>/ev-charge-range-analyzer.git
cd ev-charge-range-analyzer
pip install -r requirements.txt
python main.py
```

On first run, if no dataset exists, a synthetic dataset of 500 charging
sessions across five EV models is generated automatically at
`data/sample_ev_data.csv`. Swap in your own CSV (same column schema) to
analyze real data instead.

## What it generates

Running option 2 from the menu produces five charts in `output/`:

| Chart | What it shows |
|---|---|
| `range_accuracy_by_model.png` | Estimated vs. actual range, per vehicle model |
| `charging_speed_by_charger_type.png` | Average km of range added per hour, by charger type |
| `temperature_impact.png` | How ambient temperature affects the range prediction gap |
| `battery_degradation_trend.png` | Battery degradation % and achieved range vs. battery age |
| `driving_style_vs_range.png` | Achieved range by driving style (eco/normal/aggressive) |

Option 1 prints the same underlying tables straight to the console, and
option 3 regenerates the sample dataset with a new random sample.

## Dataset schema

| Column | Description |
|---|---|
| `vehicle_model` | EV model name |
| `battery_capacity_kwh` | Usable battery capacity |
| `rated_range_km` | Manufacturer-rated range |
| `battery_age_months` | Age of the battery pack |
| `battery_degradation_pct` | Estimated capacity loss |
| `charger_type` | Home / public AC / DC fast |
| `charger_power_kw` | Charger power rating |
| `start_soc_pct` / `target_soc_pct` | State of charge at plug-in / unplug |
| `energy_added_kwh` | Energy delivered during the session |
| `charge_duration_hrs` | Session length |
| `ambient_temp_c` | Ambient temperature during the session |
| `driving_style` | Eco / Normal / Aggressive |
| `estimated_range_km` | Range predicted from SoC and rated efficiency |
| `actual_range_km` | Range actually achieved, factoring temperature + driving style |

## Roadmap ideas

- [ ] Interactive dashboard (Streamlit / Plotly Dash)
- [ ] Import real charging-session logs (OCPP / vehicle telematics)
- [ ] Per-trip range prediction model
- [ ] Charging cost analysis by tariff/time-of-day
- [ ] Unit tests for `analysis.py`

## License

MIT — see [LICENSE](LICENSE).

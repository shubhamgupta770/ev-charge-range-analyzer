"""
EV Charge & Range Analysis Tool
=================================
A visualization tool for analyzing electric vehicle charging behavior
and real-world range performance.

Usage:
    python main.py
"""

from pathlib import Path

from src.data_loader import load_data, DEFAULT_DATA_PATH
from src.generate_sample_data import generate
from src import analysis, visualizer


def ensure_data():
    if not DEFAULT_DATA_PATH.exists():
        print("No dataset found — generating a sample dataset (500 sessions)...")
        generate()


def menu():
    print("\n===== EV Charge & Range Analysis Tool =====")
    print("1. Print summary report to console")
    print("2. Generate all charts (saved to output/)")
    print("3. Regenerate sample dataset")
    print("4. Exit")
    return input("Choose an option (1-4): ").strip()


def main():
    ensure_data()
    df = load_data()
    print(f"Loaded {len(df)} charging sessions across {df['vehicle_model'].nunique()} vehicle models.")

    while True:
        choice = menu()
        if choice == "1":
            analysis.print_report(df)
        elif choice == "2":
            visualizer.generate_all_charts(df)
            print(f"\nCharts saved in: {Path('output').resolve()}")
        elif choice == "3":
            generate()
            df = load_data()
            print("Dataset regenerated and reloaded.")
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Please choose 1, 2, 3 or 4.")


if __name__ == "__main__":
    main()

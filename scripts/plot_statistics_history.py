#!/usr/bin/env python3
"""
Manages the statistics history CSV and generates progress charts.
"""

from pathlib import Path
import csv
import subprocess
from datetime import datetime, timezone
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

ROOT = Path(__file__).resolve().parents[1]
CSV_FILE = ROOT / "data" / "statistics_history.csv"
OUTPUT_LIGHT = ROOT / "data" / "statistics_history_light.svg"
OUTPUT_DARK = ROOT / "data" / "statistics_history_dark.svg"

FIELDNAMES = ["commit", "date", "total_problems", "lean_formalized", 
              "oeis_linked", "total_solved", "proved", "disproved", "solved", "lean_solved"]

def get_current_commit():
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"]).decode("ascii").strip()
    except Exception:
        return ""

def update_history(stats: dict) -> bool:
    """
    Appends a new row to the history CSV if the stats differ from the last entry.
    Returns True if updated.
    """
    # Read last entry to compare
    last_stats = {}
    if CSV_FILE.exists():
        with CSV_FILE.open("r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
            if rows:
                last_stats = {k: int(v) for k, v in rows[-1].items() if k in stats}

    # Compare (ignoring date/commit)
    if last_stats == stats:
        return False

    # Prepare new row
    timestamp = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %z")
    row = {"commit": get_current_commit(), "date": timestamp, **stats}
    
    # Append to file
    mode = "a" if CSV_FILE.exists() else "w"
    with CSV_FILE.open(mode, encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if mode == "w":
            writer.writeheader()
        writer.writerow(row)
        
    return True

def create_plot(dates, lean_counts, oeis_counts, solve_counts, lean_solved_counts, open_counts, theme='light'):
    """Creates a progress chart figure with the specified theme (light or dark)."""

    # Theme configuration
    is_dark = theme == 'dark'
    colors = {
        'bg': '#0d1117' if is_dark else 'white',
        'text': '#c9d1d9' if is_dark else '#24292f',
        'grid': '#30363d' if is_dark else '#d0d7de',
        'box_bg': '#161b22' if is_dark else '#f6f8fa',
        'lines': ['#58a6ff', '#f85149', '#3fb950', '#d29922', '#9467bd'] if is_dark else ['#0969da', '#cf222e', '#1a7f37', '#bf8700', '#9467bd']
    }

    fig, ax = plt.subplots(figsize=(12, 7), facecolor=colors['bg'])
    ax.set_facecolor(colors['bg'])

    # Plot lines
    data = [
        (solve_counts, "Solved", colors['lines'][2]),
        (lean_counts, "Lean Formalized Problem", colors['lines'][0]),
        (lean_solved_counts, "Lean Formalized Solution", colors['lines'][3]),
        (oeis_counts, "OEIS Linked", colors['lines'][1]),
        (open_counts, "Open Problems", colors['lines'][4]),
    ]
    
    for counts, label, color in data:
        ax.plot(dates, counts, label=label, linewidth=2, color=color)
        # Add data point label at the end of each line
        if counts:
            last_value = counts[-1]
            last_date = dates[-1]
            ax.annotate(f'{last_value}', xy=(last_date, last_value), xytext=(5, 0),
                       textcoords='offset points', fontsize=9, color=color,
                       fontweight='bold', va='center')

    # Styling
    ax.set_xlabel("Date", fontsize=12, color=colors['text'])
    ax.set_ylabel("Count", fontsize=12, color=colors['text'])
    ax.set_title("Erdős Problems Progress", fontsize=14, fontweight='bold', color=colors['text'], pad=20)
    
    legend = ax.legend(loc='upper left', fontsize=10, facecolor=colors['box_bg'], edgecolor=colors['grid'])
    plt.setp(legend.get_texts(), color=colors['text'])
    
    ax.grid(True, alpha=0.25, color=colors['grid'], linewidth=0.5)
    
    # Date formatting
    locator = mdates.AutoDateLocator(minticks=5, maxticks=10)
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    
    ax.tick_params(axis='x', colors=colors['text'])
    ax.tick_params(axis='y', colors=colors['text'])
    
    for spine in ax.spines.values():
        spine.set_edgecolor(colors['grid'])

    plt.tight_layout()
    return fig

def generate_charts():
    """Reads history and generates SVG charts."""
    if not CSV_FILE.exists():
        return

    data_points = []
    with CSV_FILE.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data_points.append({
                'date': datetime.strptime(row["date"], "%Y-%m-%d %H:%M:%S %z"),
                'lean': int(row["lean_formalized"]),
                'oeis': int(row["oeis_linked"]),
                'solve': int(row["total_solved"]),
                'lean_solved': int(row.get("lean_solved", 0)),
                'open': int(row.get("open", 0))
            })

    if not data_points:
        return

    data_points.sort(key=lambda x: x['date'])

    dates = [p['date'] for p in data_points]
    lean = [p['lean'] for p in data_points]
    oeis = [p['oeis'] for p in data_points]
    solve = [p['solve'] for p in data_points]
    lean_solved = [p['lean_solved'] for p in data_points]
    open_counts = [p['open'] for p in data_points]

    for theme, path in [('light', OUTPUT_LIGHT), ('dark', OUTPUT_DARK)]:
        fig = create_plot(dates, lean, oeis, solve, lean_solved, open_counts, theme=theme)
        fig.savefig(path, format='svg', bbox_inches='tight', facecolor=fig.get_facecolor())
        plt.close(fig)

if __name__ == "__main__":
    generate_charts()

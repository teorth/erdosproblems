#!/usr/bin/env python3
"""
Manages the statistics history CSV and generates progress charts.
"""

from pathlib import Path
import csv
import subprocess
from datetime import datetime, timedelta, timezone
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

ROOT = Path(__file__).resolve().parents[1]
CSV_FILE = ROOT / "data" / "statistics_history.csv"
OUTPUT_LIGHT = ROOT / "data" / "statistics_history_light.svg"
OUTPUT_DARK = ROOT / "data" / "statistics_history_dark.svg"

# The first rows of the history (2025-08-31, roughly 10:00 to 12:10 Pacific) were
# written while the problem set was still being imported: the total went from
# 2 to 992 and the solved count from 1 to 355 within a few hours.  Those rows
# are kept in the CSV as a record but make no sense on the chart, where they
# show up as vertical lines at the left edge.  Plot from the first row with
# complete data.
PLOT_START = datetime(2025, 8, 31, 12, 49, 49, tzinfo=timezone(timedelta(hours=-7)))

FIELDNAMES = ["commit", "date", "total_problems", "lean_formalized", 
              "oeis_linked", "total_solved", "proved", "disproved", "solved", "lean_solved", "open"]

def _as_int(value, default=0):
    """Read a CSV cell that may be missing or blank.

    ``csv.DictReader`` creates a key for every column in the header and fills it
    with ``None`` on a short row, so ``row.get(name, default)`` never falls back
    for a column the header declares.  Rows written before a column existed are
    exactly that case.
    """
    if value is None or value == "":
        return default
    return int(value)


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
                last_stats = {
                    k: _as_int(v) for k, v in rows[-1].items() if k in stats
                }

    # Compare (ignoring date/commit)
    if last_stats == stats:
        return False

    # Prepare new row
    timestamp = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %z")
    row = {"commit": get_current_commit(), "date": timestamp, **stats}
    
    # Append to file
    mode = "a" if CSV_FILE.exists() and CSV_FILE.stat().st_size > 0 else "w"
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
    # Anchor at zero; scale the ceiling to the data so growing series never clip.
    max_count = max((max(counts) for counts, _, _ in data if counts), default=0)
    ax.set_ylim(0, max(max_count * 1.05, 1))
    # Start the x-axis at the first plotted date instead of matplotlib's default margin.
    if dates:
        ax.set_xlim(left=dates[0])
    
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
            date = datetime.strptime(row["date"], "%Y-%m-%d %H:%M:%S %z")
            if date < PLOT_START:
                continue
            total = _as_int(row.get("total_problems"))
            solved = _as_int(row.get("total_solved"))
            data_points.append({
                'date': date,
                'lean': _as_int(row.get("lean_formalized")),
                'oeis': _as_int(row.get("oeis_linked")),
                'solve': solved,
                'lean_solved': _as_int(row.get("lean_solved")),
                'open': _as_int(row.get("open"), total - solved)
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

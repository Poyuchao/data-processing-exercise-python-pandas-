# Data Processing — Python & pandas

Data processing with **pandas**.

## What's covered

- Loading CSV and JSON files, including UTF-8 with BOM and Chinese column headers
- Cleaning text: inconsistent case, extra spaces, IDs written different ways
- Converting types with `pd.to_numeric` / `pd.to_datetime` (`errors="coerce"`) and reporting what failed
- Parsing several time and date formats (`HH:MM:SS`, `mm:ss`, integer seconds, `dd/mm/yyyy`, `YYYY-MM-DD`)
- Combining sources with different formats into one table
- Collecting invalid rows in a "bad rows" list with a reason for each
- Removing duplicates and keeping the latest record per ID
- Flattening nested JSON
- `groupby` aggregations: distinct counts (`nunique`), means, shares
- Joins with `merge`, including finding unmatched rows on both sides
- Plain-Python parsing with `ValueError` handling, plus `pytest` tests

## Repository layout

| Folder | Contents |
|--------|----------|
| [`advisory_sessions/`](advisory_sessions/) | Doctor advisory sessions from 3 markets (UK / TW / US): merge, clean, map themes, dedupe, join profiles |
| [`clinician_feedback/`](clinician_feedback/) | UK / US clinician feedback from two systems merged into one table, with topic and sentiment summaries |
| [`lab_reference_ranges/`](lab_reference_ranges/) | Lab results checked against reference ranges (low / normal / high / unknown) per test |
| [`adverse_events/`](adverse_events/) | Adverse-event reports: days to report, late reports, per-drug summary with drug class |
| [`theme_analysis/`](theme_analysis/) | Doctor theme analysis with built-in result checks (PASS / FAIL) |
| [`clinic_visits/`](clinic_visits/) | Clinic visit analysis with groupby and merges, with built-in result checks |
| [`data_quality_tasks/`](data_quality_tasks/) | Five data-quality tasks: messy survey, nested JSON, two-table join, latest record per ID, log parsing |
| [`notebooks/`](notebooks/) | Jupyter notebooks for basic pandas exploration of an orders dataset |
| `check_env.py` | Quick check that Python, pandas and numpy are installed |

Each folder has its own `README.md` with the input files and requirements.

## Getting started

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install pandas numpy pytest
python check_env.py
```

Scripts read their data with relative paths, so run each one from inside its own folder:

```bash
cd lab_reference_ranges
python lab_status.py
```

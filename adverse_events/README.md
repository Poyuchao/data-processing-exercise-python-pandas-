# Adverse Events — Reporting Delay by Drug

A safety team logs adverse events (side effects) for several drugs. The text is messy and a few
values are broken. A second file gives the class of each drug.

Code: [`adverse_events.py`](adverse_events.py)

## Input files

| File | Columns |
|------|---------|
| `events.csv` | `event_id, patient, drug, severity, onset_date, report_date` (dates are `YYYY-MM-DD`) |
| `drugs.csv` | `drug, class` |

## Requirements

1. Load `events.csv` and clean it:
   - `drug`: remove spaces, lower case
   - `severity`: remove spaces, lower case
   - `onset_date` and `report_date`: make them real dates; invalid ones become missing
   - `event_id` can appear twice: keep the last row for each `event_id`

   Print how many rows are left after cleaning.
2. Add a column `days_to_report` = `report_date` minus `onset_date` (in days, as a number),
   and a column `late` that is `True` when `days_to_report` is more than 7.
   Rows with a missing date have `late = False`.
3. For each drug: number of events, share of events with severity `severe`, and mean
   `days_to_report`. Add the drug class from `drugs.csv` and sort by number of events
   (most first).

## Follow-up considerations

- One drug has no class in `drugs.csv`: how to find it, and what the summary shows for it.
- A `report_date` that is before the `onset_date`: how to detect it and what to do with it.

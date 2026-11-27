# Lab Results vs. Reference Ranges

A lab sends results as a CSV. The text is messy (spaces, mixed case) and some values are not
numbers. A second small file has the normal range for each test.

Code: [`lab_status.py`](lab_status.py)

## Input files

| File | Columns |
|------|---------|
| `lab_results.csv` | `patient_id, test, value, visit_date` |
| `reference_ranges.csv` | `test, low, high` |

## Requirements

1. Load `lab_results.csv` and clean it:
   - `patient_id`: remove spaces, upper case (`P001`)
   - `test`: remove spaces, lower case (`glucose`)
   - `value`: make it a number; things like `N/A` or `high` become missing

   Print how many values could not be converted.
2. Add the normal range to each row (from `reference_ranges.csv`) and add a column `status`:
   `low` if value < low, `high` if value > high, `normal` otherwise.
   Rows without a value or without a range get `unknown`.
3. For each test: number of distinct patients, mean value, and the share of rows with status
   `high` or `low`.

## Follow-up considerations

- Some tests have no reference range: how they are handled, and how to list them.
- How to check that the result is right.

# Clinician Feedback — UK / US Merge

Feedback from clinicians in two markets (UK and US). The two files come from different systems,
so the formats differ.

Code: [`feedback_pipeline.py`](feedback_pipeline.py)

## Input files

| File | Notes |
|------|-------|
| `feedback_uk.csv` | Dates are `dd/mm/yyyy`; sentiment is text (Positive / negative / NEUTRAL ...) |
| `feedback_us.json` | Dates are `YYYY-MM-DD`; sentiment is a number from 1 to 5 |

## Requirements

1. Load both files into one table with the columns
   `market, clinician, date, topic, sentiment, words`
   (in the US data, 4–5 is positive, 3 is neutral, 1–2 is negative).
2. Clean it:
   - Clinician IDs should look like `Dr_K1` (fix case and spaces).
   - Topics: lower case, no extra spaces, and `side-effects` should be `side effects`.
   - Rows with a missing clinician or an invalid date go to a "bad rows" list with a reason
     (count each row once: check the clinician first, then the date).
   - Remove duplicates on (market, clinician, date, topic), keeping the last one.
3. For each topic: how many distinct clinicians raised it, and how many mentions?
4. For each market: what share of the feedback is negative?

## Follow-up considerations

- How to check that topic names are consistent across sources.
- What changes if a third market arrives with yet another date format.

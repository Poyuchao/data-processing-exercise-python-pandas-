# Advisory Sessions — Multi-Market Theme Analysis

Advisory sessions with doctors in three markets (UK, TW, US). Each session file lists the themes
that doctors raised, with a quote and the time it came up in the session.
The three files come from different sources, so their formats differ.

Code: [`sessions_pipeline.py`](sessions_pipeline.py)

## Input files

| File | Notes |
|------|-------|
| `uk_sessions.json` | JSON list; time as `HH:MM:SS` |
| `tw_sessions.csv` | CSV with Chinese headers (UTF-8 with BOM); time as `mm:ss` |
| `us_sessions.csv` | CSV; time as integer seconds |
| `doctors.csv` | Doctor profiles (specialty, years in practice) |

## Requirements

1. Load the three session files into one table with the columns
   `market, session, doctor, seconds, theme_raw, text`.
2. Clean it:
   - Doctor IDs should look like `Dr_U1` (fix case and spaces).
   - Rows with a missing doctor, or a time that is not valid, go to a "bad rows" list with the
     reason (count each row once; check the doctor first, then the time).
     A valid time has minutes and seconds between 00 and 59.
   - Map the raw themes to 5 themes: `hypoglycemia`, `price_reimbursement`, `adherence`,
     `weight_gain`, `dosing_convenience`.
   - Remove duplicates on (market, doctor, seconds, theme), keeping the last one.
3. For each theme: how many distinct doctors raised it, and how many mentions?
4. For each market: what share of the doctors raised each theme?
5. Join `doctors.csv`:
   - Which doctors in the sessions have no profile? Which profiles have no sessions?
   - Among the doctors who raised hypoglycemia, how many are there per specialty?

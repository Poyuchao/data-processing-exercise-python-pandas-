# Data Quality Tasks

Five small data-quality tasks, each on its own input file.

## 1. Messy survey (`survey.csv`) — pandas basics

1. Load it. Print the shape and the number of missing values per column.
2. Clean the country column so `UK` / `uk` / `" uk "` are the same.
3. Make score numeric. Which raw score values could not be converted?
4. Average score per country (ignore the invalid ones), rounded to 2 decimals.
5. Parse the date column. Which respondents have a date that cannot be parsed?
   (Dates come in two formats, and some have extra spaces.)

## 2. Nested JSON (`doctor_themes.json`) — flatten + distinct counts

1. Turn it into one row per (doctor, theme). Themes differ in case and spaces, and some doctors
   have an empty list, `null`, or no `themes` key at all.
2. Remove duplicate (doctor, theme) pairs.
3. For each theme, how many distinct doctors raised it?
4. Which doctors raised no theme at all?
5. The top 3 themes by distinct doctors (break ties alphabetically).

## 3. Join two tables (`prescriptions.csv`, `doctor_profiles.csv`)

1. The doctor IDs are written differently in the two files. Make them match.
2. Which prescription rows have no doctor profile? Which profiles have no prescriptions?
3. Total qty per specialty. How much qty could not be assigned to a specialty?
4. For each specialty, which doctor has the highest total qty?

## 4. Latest record per ID (`lab_results.csv`)

1. Some samples were measured more than once. Keep only the latest measurement per sample.
2. How many samples were measured more than once?
3. For samples with more than one measurement, which ones changed by more than 10% between the
   first and the last measurement? Report the % change.
   (The rows are not in time order.)

## 5. Plain Python, no pandas (`session_log.txt`)

Each line should look like `timestamp | doctor | theme | quote`.

1. Write `parse_line(line)` that returns a dict, or raises `ValueError` with a reason.
   The quote may contain a `|` itself. Doctor IDs should look like `Dr_U1`.
2. Read the file. Keep the good rows; collect bad lines with the line number and reason.
3. Count mentions per theme (case-insensitive) and distinct doctors per theme.
4. Write two `pytest` tests for `parse_line` (one good line, one bad line).

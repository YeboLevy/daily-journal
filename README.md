# Daily Journal

A command-line journaling app built in Python as a Week 1 review project.

## Features

- Add a new journal entry with date, mood, and text
- View all past entries
- Filter entries by mood (happy / neutral / sad)
- Mood summary with a bar chart
- Search entries by keyword

## Usage

```
python3 journal.py
```

Then choose from the menu:

```
================================
         DAILY JOURNAL
================================
  1. Add new entry
  2. View all entries
  3. View entries by mood
  4. Mood summary
  5. Search by keyword
  6. Quit
================================
```

Entries are saved to `journal.json` in the same directory.

## Concepts Covered

| Concept | Where used |
|---|---|
| Variables | Constants, date, mood counts |
| Functions | Each feature is its own function |
| Loops | Menu loop, input validation, iterating entries |
| Lists | Storing entries, list comprehensions for filtering |
| Dictionaries | Each entry is a dict; mood tallying |
| File I/O | Reading and writing `journal.json` |
| Error handling | `try/except` for file ops and keyboard interrupts |

## Requirements

Python 3.6+. No external dependencies.

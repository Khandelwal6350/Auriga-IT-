# 75-Day Habit Tracker

A terminal-based, SQLite-powered habit tracker built in Python for managing daily routines, progress tracking, streaks, and morning reminders.

This project is designed to be generic and reusable for any user and any set of habits. It is a simple console application with no web frontend, no browser notifications, and no unnecessary dependencies.

---

## Project Overview

The application helps users manage multiple habits such as drinking water, reading, working out, studying, meditating, and so on. Each habit can follow a different schedule:

- Every day
- Weekdays only
- Custom days such as Monday, Wednesday, Friday

The program lets users:

- add habits
- update habit details
- complete habits for today
- view today's scheduled habits
- check current and best streaks
- search habits by name
- archive and restore habits
- review completion history
- track 75-day challenge progress
- get a terminal-based morning reminder for incomplete habits
- import and clean seat-class price lists from CSV files

This is a simple, clean, interview-friendly Python project built specifically for the Auriga IT Builder Round.

---

## Why This Project Exists

The core challenge is not only tracking habits, but tracking them correctly.

A habit should be counted only on the dates it is actually scheduled. For example:

- a Monday/Wednesday/Friday habit should not be treated as missed on Tuesday
- a weekday habit should ignore weekends
- daily habits should count every day
- custom schedules must be respected when calculating streaks and reminders

This project solves that by using a schedule-aware engine instead of a simple day-by-day comparison.

---

## Features

### Habit Management

- Add a habit with name, description, schedule, start date, and optional end date
- Update habit name, description, schedule, start date, and end date
- Archive habits without deleting them permanently
- Restore archived habits later
- Search habits by name (case-insensitive)
- View all active and archived habits

### Completion Tracking

- Mark a habit as completed for a date
- Prevent duplicate completion on the same date
- View today's habits
- View habit completion history
- See whether a habit is pending or completed for a day

### Streak Logic

- Current streak is based on consecutive scheduled completions only
- Best streak is calculated across the full habit history
- Non-scheduled days do not break the streak
- Daily, weekday, and custom schedules are all supported

### Morning Reminder

When the app starts during the morning time window, it shows a reminder for habits that are:

- active
- scheduled for today
- not already completed
- not archived
- within valid start and end dates

It prints a simple terminal reminder like this:

```text
========================================
       MORNING HABIT REMINDER
========================================
Good morning! You still have 2 habits to complete today:
1. Drink Water
2. Workout

Complete them from the main menu.
========================================
```

If all scheduled habits are already complete:

```text
========================================
       MORNING HABIT REMINDER
========================================
Great! All scheduled habits for today are completed.
========================================
```

If no habits are scheduled:

```text
========================================
       MORNING HABIT REMINDER
========================================
No habits are scheduled for today.
========================================
```

---

## Technology Stack

- Python 3
- SQLite
- Standard Python libraries only
- unittest for testing

This project intentionally avoids unnecessary dependencies and external packages.

---

## Project Structure

```text
/workspaces/Auriga-IT-
├── .gitignore
├── AI_LOGS.md
├── README.md
├── REASONING.md
├── database.py
├── habit_tracker/
│   ├── __init__.py
│   ├── habit_manager.py
│   ├── price_list.py
│   └── streak.py
├── main.py
├── requirements.txt
├── tests/
│   ├── test_reminder.py
│   └── test_streak.py
└── habit_tracker.db   # auto-created SQLite database
```

### File responsibilities

- `main.py` – terminal menu and user flow
- `database.py` – SQLite connection and table creation
- `habit_tracker/habit_manager.py` – add, update, archive, search, complete, and history logic
- `habit_tracker/price_list.py` – CSV price-list parsing, cleaning, validation, and deduplication
- `habit_tracker/streak.py` – schedule-aware streak calculations
- `tests/test_streak.py` – core streak tests
- `tests/test_reminder.py` – reminder-specific tests
- `README.md` – project documentation
- `REASONING.md` – engineering notes and design reasoning
- `AI_LOGS.md` – AI conversation/logs file according to project requirements
- `requirements.txt` – no external dependencies required
- `.gitignore` – ignores Python cache and local DB artifacts

---

## Requirements

- Python 3.9+
- SQLite support built into Python
- No external packages required

---

## Installation

1. Go to the project folder.
2. Create a virtual environment if you want an isolated setup.
3. Install dependencies if needed.

Example:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Since this project uses only the standard library, the installation step is minimal.

---

## Running the Application

From the project root, run:

```bash
python main.py
```

This will show the main terminal menu:

```text
========================================
       75-DAY HABIT TRACKER
       Krishna Khandelwal
========================================

1. View Today's Habits
2. Add Habit
3. Update Habit
4. Complete Habit
5. View Habit Streak
6. Search Habit
7. View All Habits
8. Archive Habit
9. Restore Habit
10. View Habit History
11. View 75-Day Challenge Progress
12. Import Seat-Class Price List
13. Exit
========================================
```

---

## Running Tests

This project uses Python's built-in unittest runner:

```bash
python -m unittest discover -s tests -v
```

The test suite covers:

- daily streaks
- weekday streaks
- custom schedule streaks
- broken streak behavior
- non-scheduled days not breaking streaks
- reminder pending behavior
- seat-class price parsing and CSV cleaning
- case-insensitive price-list deduplication
- invalid, blank, and negative price rejection
- archived habits exclusion
- future habit exclusion
- ended habit exclusion
- duplicate completion prevention

---

## Database

The application uses SQLite to persist data locally in a file named `habit_tracker.db`.

The database is created automatically if it does not already exist.

### Tables used

- `habits`
  - id
  - name
  - description
  - schedule_type
  - schedule_days
  - start_date
  - end_date
  - archived
  - created_at

- `completions`
  - id
  - habit_id
  - completion_date
  - completed_at
  - unique constraint on `(habit_id, completion_date)`

- `challenge`
  - id
  - start_date
  - duration

This keeps the system lightweight, portable, and easy to maintain.

---

## Streak Logic

The streak algorithm is designed to work on scheduled dates instead of plain calendar gaps.

### Current streak

Current streak counts the number of consecutive scheduled occurrences that were completed.

Example for Monday/Wednesday/Friday:

- Monday: completed
- Tuesday: not scheduled
- Wednesday: completed
- Thursday: not scheduled
- Friday: completed

Current streak = 3

### Best streak

Best streak is the longest run of completed scheduled occurrences across the full history of the habit.

### Important rule

Non-scheduled days do not break the streak.

---

## Morning Reminder Logic

The reminder uses the same scheduling logic as the rest of the app.

It checks:

- active habits only
- scheduled habits for today only
- completed versus incomplete habits
- start date validity
- end date validity
- archived status

The reminder does not create completion records; it only reads the data. It is a terminal reminder and does not depend on any browser or desktop notifications.

---

## Seat-Class Price List Import

The menu option `Import Seat-Class Price List` reads a CSV file with these columns:

```csv
seat_class,price
Economy,"1,200"
Business,₹2500.00
First Class,3500/-
```

The importer cleans whitespace, commas, the rupee symbol, the `/-` suffix, and decimal prices. Clean names are returned in Title Case and prices are returned as floats.

Case-insensitive duplicate names such as `Economy`, `economy`, and `ECONOMY` are treated as one class. Invalid rows are rejected with a reason. When multiple valid prices exist for one class, the last valid row is imported and earlier valid rows are reported as deduplicated.

The terminal report shows the number and values imported, deduplicated class names and reasons, and rejected class names with validation reasons.

---

## Validation and Error Handling

The app handles invalid user input without crashing.

Examples:

- empty habit name
- invalid date
- invalid schedule type
- invalid custom weekday names
- future start date
- end date before start date
- invalid menu choice
- duplicate completion attempt
- invalid habit ID

---

## Debugging

Common issues:

- bad date format: use `YYYY-MM-DD`
- duplicate completion: app prevents it automatically
- invalid schedule: custom schedule must use valid weekdays
- habit not showing: check if the habit is archived, future-dated, or outside its end date
- no reminder: app only reminds during the morning time window

---

## Future Improvements

Possible future enhancements include:

- habit categories
- CSV export/import
- better reporting and charts
- custom reminder time settings
- monthly summaries

These are optional and not required for the current project scope.

---

## Author

Krish Khandelwal

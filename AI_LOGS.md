I have a 2.5-hour coding assessment for Auriga IT Builder Round.

I need to build the following problem:

"Ananya’s 75-day challenge

Ananya has started a 75-day self-improvement challenge — drink water,
read, work out, no sugar. She’s juggling several habits at once:
some she does every day, some only on weekdays.

Each morning she just wants to see today’s habits and tick them off
one by one.

She’s fiercely proud of her streaks and genuinely gutted when she
breaks one, so for every habit she wants to know her current streak
and her best-ever streak.

Weeks in, her list has grown long — there are a couple she’s quietly
given up on and wants out of the way (but not gone forever), and she
keeps hunting for a particular one to update it.

Build Ananya something so she keeps her streaks alive.

The application should be generic and work for any user and any
habits, not only Ananya."

IMPORTANT:

I do NOT want HTML, CSS, React, Streamlit, or a web application.

Build a NORMAL TERMINAL/CONSOLE BASED Python application.

Use:

- Python
- SQLite
- Standard Python libraries wherever possible

Keep the project simple, clean, reliable and easy to explain in an
interview.

Do NOT over-engineer the project.

==================================================
CORE REQUIREMENTS
==================================================

Create a menu-driven Habit Tracker application.

When I run:

python main.py

the application should show a menu such as:

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
12. Exit

The user can select options from the terminal.

==================================================
1. ADD HABIT
==================================================

Allow the user to create a habit.

Store:

- habit ID
- habit name
- description
- schedule
- start date
- end date
- archived status
- created date

Schedule options:

1. Every day
2. Weekdays
3. Custom days

For custom days allow:

Monday
Tuesday
Wednesday
Thursday
Friday
Saturday
Sunday

Example:

Habit:
Drink Water

Schedule:
Every day

Another:

Workout

Schedule:
Monday, Wednesday, Friday

==================================================
2. VIEW TODAY'S HABITS
==================================================

This is the main feature.

When the user selects:

View Today's Habits

show only ACTIVE habits that are scheduled for today.

Example:

Today's Date: 2026-09-16

1. Drink Water       [Completed]     Current: 5 days
2. Read Book         [Pending]       Current: 3 days
3. Workout           [Pending]       Current: 2 days

The user should immediately know what needs to be completed today.

Archived habits must NOT appear in today's active list.

==================================================
3. COMPLETE HABIT
==================================================

Allow the user to select a habit and mark it completed for today.

Example:

Enter habit ID: 2

Habit "Read Book" marked as completed.

Do not allow duplicate completion for the same habit on the same date.

If the habit has already been completed today, display:

Habit is already completed today.

==================================================
4. CURRENT STREAK
==================================================

Calculate the current streak correctly.

Current streak means consecutive SCHEDULED occurrences that have
been completed.

IMPORTANT:

Do NOT simply compare yesterday and today.

The algorithm must understand the habit schedule.

Example:

Schedule:
Monday, Wednesday, Friday

Completion:

Monday      YES
Tuesday     -
Wednesday   YES
Thursday    -
Friday      YES

Current streak = 3

Tuesday and Thursday should not break the streak because they are not
scheduled days.

==================================================
5. BEST-EVER STREAK
==================================================

For every habit calculate the maximum number of consecutive scheduled
occurrences that were completed in the entire history.

Example:

Monday       YES
Wednesday    YES
Friday       YES
Monday       YES
Wednesday    NO
Friday       YES

Best streak should be calculated from the completed scheduled
occurrences.

Store completion history in SQLite and calculate the streak from the
history reliably.

==================================================
6. SEARCH HABIT
==================================================

Allow the user to search by habit name.

Example:

Search:
water

Results:

1. Drink Water
2. Drink Green Tea

Search should be case-insensitive.

==================================================
7. UPDATE HABIT
==================================================

Allow the user to update:

- habit name
- description
- schedule
- start date
- end date

Do not delete historical completion records when updating a habit.

==================================================
8. ARCHIVE HABIT
==================================================

The problem says some habits are given up but should not be gone
forever.

Therefore implement ARCHIVE.

When archived:

- habit is hidden from active/today list
- historical data remains
- user can view archived habits
- user can restore the habit later

Do NOT permanently delete it.

==================================================
9. RESTORE HABIT
==================================================

Allow the user to restore an archived habit.

After restoring, it should appear again if it is scheduled for today.

==================================================
10. HABIT HISTORY
==================================================

Allow the user to view completion history.

Example:

Habit: Workout

2026-09-10   Completed
2026-09-11   Not scheduled
2026-09-12   Not scheduled
2026-09-13   Completed

Only scheduled dates need to be considered for streak calculation.

==================================================
11. 75-DAY CHALLENGE
==================================================

Implement a simple 75-day challenge progress system.

Store challenge start date.

Calculate:

- current challenge day
- completed challenge days
- remaining days
- progress percentage

Example:

========================================
75-DAY CHALLENGE
========================================

Start Date: 2026-08-01
Today: 2026-09-16

Challenge Day: 47 / 75
Remaining: 28 days
Progress: 62.67%

Keep this generic so the user can change the challenge start date.

==================================================
12. DATABASE
==================================================

Use SQLite.

Create database automatically if it does not exist.

Suggested tables:

habits

- id INTEGER PRIMARY KEY AUTOINCREMENT
- name TEXT NOT NULL
- description TEXT
- schedule_type TEXT NOT NULL
- schedule_days TEXT
- start_date TEXT NOT NULL
- end_date TEXT
- archived INTEGER DEFAULT 0
- created_at TEXT NOT NULL

completions

- id INTEGER PRIMARY KEY AUTOINCREMENT
- habit_id INTEGER NOT NULL
- completion_date TEXT NOT NULL
- completed_at TEXT NOT NULL
- FOREIGN KEY(habit_id) REFERENCES habits(id)
- UNIQUE(habit_id, completion_date)

challenge

- id INTEGER PRIMARY KEY
- start_date TEXT NOT NULL
- duration INTEGER DEFAULT 75

Use parameterized SQL queries.

==================================================
13. PROJECT STRUCTURE
==================================================

Keep the project simple.

Use:

habit_tracker/
│
├── main.py
├── database.py
├── habit_manager.py
├── streak.py
├── README.md
├── REASONING.md
├── AI_LOGS.md
├── requirements.txt
├── .gitignore
└── tests/
    └── test_streak.py

Avoid unnecessary folders and dependencies.

==================================================
14. CODE DESIGN
==================================================

Separate responsibilities.

main.py
- terminal menu
- user input
- display output

database.py
- SQLite connection
- table creation
- database queries

habit_manager.py
- add habit
- update habit
- archive
- restore
- search
- today's habits
- completion

streak.py
- scheduled date logic
- current streak
- best streak

tests/test_streak.py
- streak tests

==================================================
15. STREAK ALGORITHM
==================================================

This is the most important business logic.

Create a clean function such as:

calculate_current_streak(habit, completion_dates)

and:

calculate_best_streak(habit, completion_dates)

The algorithm must:

1. Understand the habit schedule.
2. Generate scheduled dates.
3. Check which scheduled dates are completed.
4. Ignore non-scheduled dates.
5. Calculate consecutive completed scheduled occurrences.
6. Calculate current streak.
7. Calculate best-ever streak.

Handle:

- daily habits
- weekday habits
- custom schedules
- future start dates
- end dates
- broken streaks
- restarted streaks

Document the algorithm clearly in REASONING.md.

==================================================
16. VALIDATION
==================================================

Validate:

- empty habit name
- invalid date
- invalid menu choice
- invalid habit ID
- duplicate completion
- invalid schedule
- future start date
- end date before start date

The program should not crash because of normal invalid user input.

==================================================
17. TESTING
==================================================

Write tests for:

- daily habit streak
- weekday streak
- custom schedule
- broken streak
- best-ever streak
- current streak
- non-scheduled days
- duplicate completion

Use Python unittest or pytest.

Prefer unittest if no external dependency is necessary.

==================================================
18. README.md
==================================================

Create a professional README.md.

Include:

# 75-Day Habit Tracker

## Project Overview

## Features

## Technology Stack

## Project Structure

## Requirements

## Installation

## Running the Application

python main.py

## Running Tests

python -m unittest discover

## Database

Explain SQLite database.

## How Streaks Work

Explain the algorithm at a high level.

## Debugging

Give common problems and solutions.

## Future Improvements

## Author

Krishna Khandelwal

Do not claim features that are not implemented.

==================================================
19. REASONING.md
==================================================

Create REASONING.md.

Do NOT provide hidden chain-of-thought.

Instead write an engineering decision document explaining:

- How the problem statement was interpreted
- Requirements derived from the statement
- Why a terminal application was selected
- Why SQLite was selected
- Data model
- Scheduling design
- Streak calculation design
- Current streak
- Best streak
- Archive design
- Search design
- Validation
- Testing
- Edge cases
- Trade-offs
- Future improvements

==================================================
20. AI_LOGS.md
==================================================

DO NOT fabricate AI logs.

The company requires the COMPLETE AI conversation.

The actual AI conversation used during development must be copied into
AI_LOGS.md exactly as required by the company.

Do not create fake conversations.

Do not summarize the AI conversation.

Do not modify the actual conversation.

==================================================
21. IMPORTANT
==================================================

This is a placement assessment.

Prioritize:

1. Working functionality
2. Correct streak logic
3. Persistent database
4. Clean code
5. Good error handling
6. Tests
7. README and REASONING
8. UI polish only if relevant

Do not add:

- Login/authentication
- Cloud database
- React
- HTML
- CSS
- REST API
- unnecessary third-party packages
- complex architecture

unless absolutely necessary.

The final project should be a NORMAL Python terminal application that
can be run directly using:

python main.py

==================================================
FINAL CHECK
==================================================

Before finishing, verify:

[ ] python main.py works
[ ] SQLite database is created automatically
[ ] Add habit works
[ ] View today's habits works
[ ] Complete habit works
[ ] Duplicate completion is prevented
[ ] Current streak is correct
[ ] Best streak is correct
[ ] Daily schedule works
[ ] Weekday schedule works
[ ] Custom schedule works
[ ] Non-scheduled days do not break streak
[ ] Update habit works
[ ] Search works
[ ] Archive works
[ ] Restore works
[ ] History works
[ ] 75-day progress works
[ ] Invalid input does not crash program
[ ] Tests pass
[ ] README.md exists
[ ] REASONING.md exists
[ ] AI_LOGS.md exists
[ ] .gitignore exists
[ ] No secrets are committed
[ ] Author is shown as Krishna Khandelwal

First explain the implementation plan briefly.

Then create the project files and code.
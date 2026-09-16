# 75-Day Habit Tracker

## Project Overview
Explain what the project does, its purpose, and how it helps users manage habits during a 75-day challenge.

## Features
Document the implemented features, including:
- Add Habit
- View Today's Habits
- Complete Habit
- Duplicate completion prevention
- Current streak
- Best-ever streak
- Daily schedule
- Weekday schedule
- Custom-day schedule
- Search Habit
- Update Habit
- Archive Habit
- Restore Habit
- Habit History
- 75-Day Challenge Progress
- Morning Habit Reminder
- Input validation
- Persistent SQLite storage

Only include features that are actually implemented.

## Morning Habit Reminder
Explain how the application reminds the user each morning about habits that are still pending for the current day.

Explain that the reminder is terminal-based and should consider:
- Active habits only
- Habits scheduled for the current day
- Habits that have started
- Habits that have not expired
- Habits that have not already been completed today
- Archived habits must be excluded

Only describe behavior that is actually implemented in the code.

## Technology Stack
Include the actual technologies used, such as:
- Python
- SQLite
- Standard Python libraries
- pytest, if used by the project tests

Do not add unnecessary technologies.

## Project Structure
Document the actual current project structure and briefly explain the responsibility of each important file.

For example, if these files exist:

habit_tracker/
├── __init__.py
├── habit_manager.py
└── streak.py

tests/
├── test_streak.py
└── test_reminder.py

main.py
database.py
README.md
REASONING.md
AI_LOGS.md
requirements.txt
.gitignore

Make sure the structure matches the actual project.

## Application Menu
Document the terminal menu and explain each option:

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

## Habit Scheduling
Explain:
- Every day
- Weekdays
- Custom days Monday-Sunday
- Start date
- End date
- How scheduled dates are determined

## Streak Calculation
Explain the implemented streak logic at a high level.

Important:
- Streaks must be schedule-aware.
- Non-scheduled days must not break a streak.
- Current streak represents consecutive completed scheduled occurrences.
- Best streak represents the maximum completed consecutive scheduled occurrences.
- Mention support for daily, weekday, and custom schedules.

Do not provide hidden chain-of-thought or internal reasoning.

## Database
Explain the SQLite database and the main tables used by the application.

Document the purpose of:
- habits
- completions
- challenge

Mention important data-integrity behavior such as preventing duplicate completion for the same habit on the same date.

## Data Persistence
Explain that habit data, completion history, archive status, and challenge information are persisted using SQLite.

## Input Validation
Document the validation implemented for:
- Empty habit names
- Invalid dates
- Invalid menu choices
- Invalid habit IDs
- Invalid schedules
- Future start dates
- End date before start date
- Duplicate completion

Only mention validations that are actually implemented.

## Testing
Document the project's automated tests.

Mention the actual test command used by the project, for example:

python -m pytest

If the current test suite has a verified test result, document the actual result only.

Do not invent test results.

## Installation

Provide the actual installation/setup steps required for the project.

If a virtual environment is recommended, explain the commands.

If requirements.txt is present, explain how to install it.

## Running the Application

Show:

python main.py

Explain that the application runs as a normal terminal/console Python application.

## Running Tests

Show the correct command based on the current project:

python -m pytest

Do not document commands that are not applicable to the current test setup.

## Error Handling
Explain how the application handles normal invalid user input without crashing.

## Design
Briefly explain the separation of responsibilities between:
- main.py
- database.py
- habit_manager.py
- streak.py
- test files

Keep this as an engineering overview, not hidden reasoning.

## Data Integrity
Explain:
- SQLite persistence
- Foreign-key relationship between habits and completions if implemented
- Unique completion protection
- Preservation of completion history
- Archive instead of permanent deletion

Only describe what the source code actually implements.

## Example Workflow
Provide a short example of how a user can:
1. Add a habit
2. View today's habits
3. Complete the habit
4. View its streak
5. View history
6. Archive/restore it

## Requirements
List the actual runtime and testing requirements.

## Project Status
Describe the current implementation status based on the actual project files and tests.

## Author

Krish Khandelwal

IMPORTANT FINAL RULES:
1. The README must contain ONLY project-related content.
2. English only.
3. Markdown only.
4. No conversational introduction or conclusion.
5. No emojis unless genuinely appropriate for a professional GitHub README.
6. No frontend/web technologies should be described because this is a terminal application.
7. Do not add features that do not exist.
8. Do not modify application code.
9. Do not fabricate test results.
10. Save the final content directly to README.md.
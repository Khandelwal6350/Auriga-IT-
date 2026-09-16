# REASONING

## How the problem statement was interpreted

The requirement describes a habit-tracking workflow focused on a terminal application where a user quickly sees today's tasks, marks them complete, and tracks behavior over time. The key interpretation was that the system must be reusable for any user and any habit, not just a single fixed list.

## Requirements derived from the statement

The core requirements are:

- a menu-driven console experience
- SQLite persistence for habits and completions
- schedule-aware habit logic
- streak calculations that ignore unscheduled days
- archive and restore behavior instead of hard deletion
- challenge tracking for a fixed 75-day duration
- validation for input and business rules
- tests covering the most important streak scenarios

## Why a terminal application was selected

A terminal-based application is the simplest way to satisfy the requirement without introducing web frameworks, HTML, CSS, or frontend tooling. It is easy to run with `python main.py`, keeps the project small, and focuses attention on correctness instead of UI complexity.

## Why SQLite was selected

SQLite fits the requirement well because it is built into Python, stores data locally, requires no server setup, and is appropriate for a single-user tracker. The persistence layer remains simple while still supporting the relational structure needed for habits, completions, and challenge state.

## Data model

The system stores three main entities:

- habits: metadata such as name, description, schedule, start date, end date, archiving state, and creation timestamp
- completions: a habit's completed dates, keyed by habit and date to prevent duplicates
- challenge: global configuration for the challenge start date and duration

This structure keeps the app generic and easy to query.

## Scheduling design

Habit schedules are normalized to three categories:

- daily
- weekday
- custom

For custom schedules, the app accepts weekdays such as Monday, Wednesday, Friday and stores them in a normalized form. The scheduler then uses the actual day-of-week to determine whether a habit is active on a particular date.

## Streak calculation design

The streak algorithm is based on scheduled dates, not on calendar-day adjacency.

1. Generate all dates on which the habit is scheduled.
2. Gather the completion dates for that habit.
3. Remove non-scheduled dates from consideration.
4. Walk backward through scheduled dates to count consecutive completed occurrences.
5. Stop when a scheduled date is missed or when no more scheduled dates remain.

This allows weekday and custom schedules to work correctly without false breaks caused by days on which the habit is not supposed to run.

## Current streak

Current streak means the total number of consecutive scheduled occurrences that are completed, ending at the most recent scheduled date in the habit history or today, whichever is relevant for the data being evaluated. It must not simply compare yesterday and today because that fails for weekly or custom schedules.

## Best streak

Best streak tracks the longest run of consecutive completed scheduled occurrences across the full history of the habit. This is calculated by iterating through the habit's scheduled dates in order and counting uninterrupted scheduled completions.

## Archive design

The archive feature is intentionally non-destructive. Archived habits remain in the database and retain their completion history, but they are hidden from active lists and today's tasks. This supports the requirement that habits may be paused without being permanently deleted.

## Search design

Search is case-insensitive and matches on the habit name. This makes it lightweight to find a habit without forcing extra schema complexity.

## Validation

Validation guards against common user errors:

- empty habit names
- invalid dates
- invalid schedule types
- invalid custom weekday names
- end dates before start dates
- future start dates
- duplicate completions
- invalid menu selection

The app catches these values and surfaces a clear error instead of crashing.

## Morning reminder design

The reminder was added to support the practical need for a simple daily nudge without introducing a background service or browser notifications. It is implemented as a terminal check that runs whenever the application starts during the morning window. The logic is intentionally separate from the menu flow so it can be reused and tested independently.

Pending habits are identified by reusing the same scheduling logic already used by the rest of the application:

1. Load only active habits.
2. Ignore habits whose start date is in the future.
3. Ignore habits whose end date has already passed.
4. Filter to habits scheduled for today.
5. Check completions for today's date.
6. Return only the ones still incomplete.

This keeps the reminder aligned with the app's existing schedule semantics and prevents duplication because completion data is checked through the same database constraints that already enforce unique entries per habit/date.

A terminal reminder was chosen because the project requirement explicitly forbids web or browser-based notifications. A background daemon would add complexity and would not match the assessment-friendly design. A simple start-of-session reminder keeps the project reliable, easy to explain, and fully compatible with a normal console application.

## Testing

The tests focus on the business-critical algorithm: streaks for daily, weekday, and custom schedules, missed scheduled days, and broken streak resets. This keeps the verification targeted and reliable.

## Edge cases

Notable edge cases include:

- habits that start in the future
- habits that have end dates
- custom schedules with repeated or invalid weekdays
- archived habits that should not appear in active lists
- duplicate completion attempts
- schedules that do not run on weekends or specific weekdays
- reminder checks during non-morning hours, when no reminder should be shown
- habits already completed today, which should be excluded from the reminder list

## Trade-offs

This project deliberately avoids over-engineering. It uses a single database file, a simple menu, and a clear separation between persistence and business logic. That keeps the application understandable and interview-friendly while still meeting the problem requirements.

## Future improvements

Potential future work includes CSV export, habit categories, overdue flags, and smarter reporting. None of these are required for this assessment, and they would not be added until the core functionality is fully correct.

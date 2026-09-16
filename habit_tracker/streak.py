"""Scheduled-date logic and streak calculations for habit tracking."""

from datetime import date, timedelta

WEEKDAY_NAMES = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


def _parse_date(value):
    if value is None or value == "":
        return None
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value))
    except ValueError:
        return None


def _normalize_schedule_days(raw_days):
    if not raw_days:
        return []
    if isinstance(raw_days, str):
        values = [part.strip() for part in raw_days.split(",") if part.strip()]
    else:
        values = []
        for item in raw_days:
            if isinstance(item, str):
                values.extend(part.strip() for part in item.split(",") if part.strip())
            else:
                values.append(str(item).strip())

    normalized = []
    seen = set()
    for value in values:
        day_name = value.title()
        if day_name not in WEEKDAY_NAMES:
            continue
        if day_name not in seen:
            normalized.append(day_name)
            seen.add(day_name)
    return normalized


def is_habit_scheduled_for_date(habit, current_date):
    """Return True only when the habit is scheduled on the given calendar date."""
    if current_date is None:
        return False

    schedule_type = (habit.get("schedule_type") or "daily").lower()
    if schedule_type in {"daily", "everyday"}:
        return True
    if schedule_type == "weekday":
        return current_date.weekday() < 5
    if schedule_type == "custom":
        scheduled_days = set(_normalize_schedule_days(habit.get("schedule_days")))
        return WEEKDAY_NAMES[current_date.weekday()] in scheduled_days
    return False


def get_scheduled_dates(habit, start_date=None, end_date=None):
    """Return the scheduled dates for the habit within a date window."""
    if not habit:
        return []

    habit_start = _parse_date(habit.get("start_date"))
    habit_end = _parse_date(habit.get("end_date"))
    if habit_start is None:
        return []

    range_start = _parse_date(start_date) if start_date else habit_start
    range_end = _parse_date(end_date) if end_date else (habit_end or date.today())
    if habit_end is not None:
        range_end = min(range_end, habit_end)
    if range_end < range_start:
        return []

    scheduled = []
    day_cursor = range_start
    while day_cursor <= range_end:
        if is_habit_scheduled_for_date(habit, day_cursor):
            scheduled.append(day_cursor)
        day_cursor += timedelta(days=1)
    return scheduled


def calculate_current_streak(habit, completion_dates):
    """Count consecutive completed scheduled occurrences ending at the latest completed scheduled date."""
    if not habit:
        return 0

    completion_set = set()
    for item in completion_dates or []:
        parsed = _parse_date(item)
        if parsed is not None:
            completion_set.add(parsed)

    if not completion_set:
        return 0

    latest_completion = max(completion_set)
    scheduled_dates = get_scheduled_dates(habit, end_date=max(date.today(), latest_completion))
    if not scheduled_dates:
        return 0

    index = len(scheduled_dates) - 1
    while index >= 0 and scheduled_dates[index] not in completion_set:
        index -= 1
    if index < 0:
        return 0

    streak = 0
    while index >= 0 and scheduled_dates[index] in completion_set:
        streak += 1
        index -= 1
    return streak


def calculate_best_streak(habit, completion_dates):
    """Best-ever streak is the longest run of completed scheduled occurrences in the habit history."""
    if not habit:
        return 0

    completion_set = set()
    for item in completion_dates or []:
        parsed = _parse_date(item)
        if parsed is not None:
            completion_set.add(parsed)

    if not completion_set:
        return 0

    end_limit = max(completion_set)
    scheduled_dates = get_scheduled_dates(habit, end_date=end_limit)
    if not scheduled_dates:
        return 0

    best_streak = 0
    current_streak = 0
    for scheduled_date in scheduled_dates:
        if scheduled_date in completion_set:
            current_streak += 1
            best_streak = max(best_streak, current_streak)
        else:
            current_streak = 0
    return best_streak

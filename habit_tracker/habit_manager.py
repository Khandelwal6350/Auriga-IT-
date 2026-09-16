"""Business logic for adding, updating, listing, archiving and completing habits."""

from datetime import date

from database import (
    add_completion,
    add_habit,
    archive_habit,
    get_all_habits,
    get_completion_dates,
    get_habit_by_id,
    restore_habit,
    search_habits,
    update_habit,
)
from habit_tracker.streak import calculate_best_streak, calculate_current_streak, is_habit_scheduled_for_date

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
    if value in (None, ""):
        return None
    try:
        return date.fromisoformat(str(value))
    except ValueError:
        return None


def _normalize_schedule_days(raw_days):
    if raw_days is None:
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
            raise ValueError(f"Invalid weekday name: {value}")
        if day_name not in seen:
            normalized.append(day_name)
            seen.add(day_name)
    return normalized


def validate_habit_data(name, schedule_type, start_date, end_date, schedule_days=None):
    if not name or not name.strip():
        raise ValueError("Habit name cannot be empty.")

    schedule_type = (schedule_type or "daily").lower()
    valid_types = {"daily", "weekday", "custom"}
    if schedule_type not in valid_types:
        raise ValueError("Invalid schedule type.")

    start_value = _parse_date(start_date)
    if start_value is None:
        raise ValueError("Invalid start date.")
    if start_value > date.today():
        raise ValueError("Start date cannot be in the future.")

    end_value = _parse_date(end_date) if end_date else None
    if end_value is not None and end_value < start_value:
        raise ValueError("End date cannot be earlier than the start date.")

    if schedule_type == "custom":
        custom_days = _normalize_schedule_days(schedule_days)
        if not custom_days:
            raise ValueError("Custom schedule requires at least one day.")

    return schedule_type


def create_habit(name, description, schedule_type, schedule_days, start_date, end_date):
    schedule_type = validate_habit_data(name, schedule_type, start_date, end_date, schedule_days)
    normalized_schedule = ""
    if schedule_type == "custom":
        normalized_schedule = ", ".join(_normalize_schedule_days(schedule_days))

    habit_id = add_habit(
        name.strip(),
        description.strip() if description else "",
        schedule_type,
        normalized_schedule,
        _parse_date(start_date).isoformat(),
        _parse_date(end_date).isoformat() if end_date else None,
    )
    return habit_id


def update_habit_record(habit_id, name=None, description=None, schedule_type=None, schedule_days=None, start_date=None, end_date=None):
    existing = get_habit_by_id(habit_id)
    if existing is None:
        raise ValueError("Invalid habit ID.")

    new_name = (name or existing["name"]).strip()
    new_description = (description if description is not None else existing["description"]) or ""
    new_schedule_type = (schedule_type or existing["schedule_type"]).lower()
    new_start_date = start_date or existing["start_date"]
    new_end_date = end_date if end_date is not None else existing["end_date"]

    if new_schedule_type == "custom":
        custom_schedule = _normalize_schedule_days(schedule_days if schedule_days is not None else existing.get("schedule_days", ""))
        if not custom_schedule:
            raise ValueError("Custom schedule requires at least one day.")
    else:
        custom_schedule = []

    validate_habit_data(new_name, new_schedule_type, new_start_date, new_end_date, ", ".join(custom_schedule) if custom_schedule else "")

    normalized_schedule = ", ".join(custom_schedule) if new_schedule_type == "custom" else ""
    update_habit(
        habit_id,
        new_name,
        new_description,
        new_schedule_type,
        normalized_schedule,
        _parse_date(new_start_date).isoformat(),
        _parse_date(new_end_date).isoformat() if new_end_date else None,
    )
    return True


def list_habits(include_archived=False):
    return get_all_habits(include_archived=include_archived)


def search_habits_by_name(search_term):
    return search_habits(search_term.strip())


def get_todays_habits(today=None):
    chosen_day = _parse_date(today) if today else date.today()
    habits = list_habits(include_archived=False)
    result = []
    for habit in habits:
        if habit.get("end_date") and _parse_date(habit["end_date"]) < chosen_day:
            continue
        if _parse_date(habit["start_date"]) > chosen_day:
            continue
        if is_habit_scheduled_for_date(habit, chosen_day):
            completion_dates = [
                _parse_date(item)
                for item in get_completion_dates(habit["id"])
            ]
            habit_copy = dict(habit)
            habit_copy["current_streak"] = calculate_current_streak(habit_copy, completion_dates)
            habit_copy["best_streak"] = calculate_best_streak(habit_copy, completion_dates)
            habit_copy["completed_today"] = any(
                completion_date == chosen_day for completion_date in completion_dates
            )
            result.append(habit_copy)
    return sorted(result, key=lambda item: item["id"])


def get_pending_today_habits(today=None):
    """Return only active, scheduled, unfinished habits for the day."""
    chosen_day = _parse_date(today) if today else date.today()
    pending = []
    for habit in list_habits(include_archived=False):
        if habit.get("end_date") and _parse_date(habit["end_date"]) < chosen_day:
            continue
        if _parse_date(habit["start_date"]) > chosen_day:
            continue
        if not is_habit_scheduled_for_date(habit, chosen_day):
            continue
        if any(_parse_date(item) == chosen_day for item in get_completion_dates(habit["id"])):
            continue
        pending.append(dict(habit))
    return sorted(pending, key=lambda item: item["id"])


def complete_habit(habit_id, completion_date=None):
    habit = get_habit_by_id(habit_id)
    if habit is None:
        raise ValueError("Invalid habit ID.")

    chosen_day = _parse_date(completion_date) if completion_date else date.today()
    if habit.get("archived") == 1:
        raise ValueError("Archived habits cannot be completed.")
    if _parse_date(habit["start_date"]) > chosen_day:
        raise ValueError("Habit start date is in the future.")
    if habit.get("end_date") and _parse_date(habit["end_date"]) < chosen_day:
        raise ValueError("Habit has already ended.")
    if not is_habit_scheduled_for_date(habit, chosen_day):
        raise ValueError("Habit is not scheduled for this date.")

    completion_value = chosen_day.isoformat()
    did_insert = add_completion(habit_id, completion_value)
    if not did_insert:
        return False, "Habit is already completed today."
    return True, f'Habit "{habit["name"]}" marked as completed.'


def archive_habit_record(habit_id):
    if get_habit_by_id(habit_id) is None:
        raise ValueError("Invalid habit ID.")
    archive_habit(habit_id)
    return True


def restore_habit_record(habit_id):
    if get_habit_by_id(habit_id) is None:
        raise ValueError("Invalid habit ID.")
    restore_habit(habit_id)
    return True


def get_habit_history(habit_id, start_date=None, end_date=None):
    habit = get_habit_by_id(habit_id)
    if habit is None:
        raise ValueError("Invalid habit ID.")

    selected_start = _parse_date(start_date) if start_date else _parse_date(habit["start_date"])
    selected_end = _parse_date(end_date) if end_date else date.today()
    if selected_end < selected_start:
        raise ValueError("End date cannot be before the start date.")

    completion_dates = set(_parse_date(item) for item in get_completion_dates(habit_id))
    records = []
    current_day = selected_start
    while current_day <= selected_end:
        if is_habit_scheduled_for_date(habit, current_day):
            if current_day in completion_dates:
                status = "Completed"
            else:
                status = "Pending"
        else:
            status = "Not scheduled"
        records.append({"date": current_day.isoformat(), "status": status})
        current_day = current_day.fromordinal(current_day.toordinal() + 1)
    return records


def get_habit_streak_summary(habit_id):
    habit = get_habit_by_id(habit_id)
    if habit is None:
        raise ValueError("Invalid habit ID.")

    completion_dates = [
        _parse_date(item) for item in get_completion_dates(habit_id)
    ]
    current_streak = calculate_current_streak(habit, completion_dates)
    best_streak = calculate_best_streak(habit, completion_dates)
    return {
        "habit": habit,
        "current_streak": current_streak,
        "best_streak": best_streak,
    }


def get_challenge_progress(start_date=None, duration=75):
    if start_date is None:
        from database import get_challenge_settings

        settings = get_challenge_settings()
        start_date = settings["start_date"]
    if duration is None:
        duration = 75

    start_day = _parse_date(start_date)
    today = date.today()
    if today < start_day:
        challenge_day = 0
    else:
        challenge_day = (today - start_day).days + 1
    if challenge_day > duration:
        challenge_day = duration

    completed_days = challenge_day
    remaining_days = max(duration - challenge_day, 0)
    progress = (completed_days / duration * 100) if duration else 0
    return {
        "start_date": start_day.isoformat(),
        "today": today.isoformat(),
        "challenge_day": challenge_day,
        "total_days": duration,
        "completed_days": completed_days,
        "remaining_days": remaining_days,
        "progress_percentage": round(progress, 2),
    }

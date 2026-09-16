"""Main terminal menu for the habit tracker application."""

from datetime import date

from database import get_challenge_settings, initialize_database, update_challenge_start_date
from habit_tracker.habit_manager import (
    complete_habit,
    create_habit,
    get_challenge_progress,
    get_habit_history,
    get_habit_streak_summary,
    get_pending_today_habits,
    get_todays_habits,
    list_habits,
    search_habits_by_name,
    update_habit_record,
    archive_habit_record,
    restore_habit_record,
)
from habit_tracker.price_list import import_price_list_from_csv


def show_menu():
    print("\n" + "=" * 40)
    print("       75-DAY HABIT TRACKER")
    print("       Krish Khandelwal")
    print("=" * 40)
    print("1. View Today's Habits")
    print("2. Add Habit")
    print("3. Update Habit")
    print("4. Complete Habit")
    print("5. View Habit Streak")
    print("6. Search Habit")
    print("7. View All Habits")
    print("8. Archive Habit")
    print("9. Restore Habit")
    print("10. View Habit History")
    print("11. View 75-Day Challenge Progress")
    print("12. Import Seat-Class Price List")
    print("13. Exit")
    print("=" * 40)


def safe_input(prompt):
    try:
        return input(prompt).strip()
    except EOFError:
        return ""


def prompt_for_schedule():
    print("Schedule options:")
    print("1. Every day")
    print("2. Weekdays")
    print("3. Custom days")
    choice = safe_input("Select schedule type: ")
    if choice == "1":
        return "daily", ""
    if choice == "2":
        return "weekday", ""
    if choice == "3":
        while True:
            days = safe_input("Enter custom days (e.g. Monday, Wednesday, Friday): ")
            if days:
                return "custom", days
            print("Custom schedule cannot be empty.")
    return "daily", ""


def show_todays_habits():
    today = date.today().isoformat()
    habits = get_todays_habits(today)
    print(f"\nToday's Date: {today}")
    if not habits:
        print("No habits scheduled for today.")
        return
    for index, habit in enumerate(habits, start=1):
        status = "[Completed]" if habit["completed_today"] else "[Pending]"
        print(f"{index}. {habit['name']:<20} {status:<12} Current: {habit['current_streak']} days")


def add_habit_flow():
    name = safe_input("Habit name: ")
    if not name:
        print("Habit name cannot be empty.")
        return

    description = safe_input("Description: ")
    schedule_type, schedule_days = prompt_for_schedule()
    start_date = safe_input("Start date (YYYY-MM-DD): ")
    end_date = safe_input("End date (YYYY-MM-DD, blank for no end date): ")

    try:
        created_id = create_habit(name, description, schedule_type, schedule_days, start_date, end_date)
        print(f"Habit added successfully with ID {created_id}.")
    except ValueError as exc:
        print(f"Error: {exc}")


def update_habit_flow():
    habits = list_habits(include_archived=True)
    if not habits:
        print("No habits found.")
        return
    for habit in habits:
        print(f"{habit['id']}. {habit['name']} ({'Archived' if habit['archived'] else 'Active'})")

    habit_id = safe_input("Enter habit ID to update: ")
    if not habit_id:
        print("Habit ID is required.")
        return

    try:
        habit_id_int = int(habit_id)
    except ValueError:
        print("Invalid habit ID.")
        return

    try:
        current = next(item for item in habits if item["id"] == habit_id_int)
    except StopIteration:
        print("Invalid habit ID.")
        return

    new_name = safe_input(f"New name ({current['name']}): ") or current['name']
    new_description = safe_input(f"New description ({current['description'] or 'none'}): ")
    if new_description == "":
        new_description = current['description'] or ""

    print("Keep current schedule by pressing Enter.")
    schedule_type, schedule_days = prompt_for_schedule()
    if schedule_type != "custom":
        schedule_days = ""
    new_start = safe_input(f"New start date ({current['start_date']}): ") or current['start_date']
    new_end = safe_input(f"New end date ({current['end_date'] or 'none'}): ")
    if new_end == "":
        new_end = current['end_date']

    try:
        update_habit_record(
            habit_id_int,
            name=new_name,
            description=new_description,
            schedule_type=schedule_type,
            schedule_days=schedule_days,
            start_date=new_start,
            end_date=new_end,
        )
        print("Habit updated successfully.")
    except ValueError as exc:
        print(f"Error: {exc}")


def complete_habit_flow():
    habit_id = safe_input("Enter habit ID: ")
    if not habit_id:
        print("Habit ID is required.")
        return
    try:
        habit_id_int = int(habit_id)
    except ValueError:
        print("Invalid habit ID.")
        return

    try:
        success, message = complete_habit(habit_id_int)
        if success:
            print(message)
        else:
            print(message)
    except ValueError as exc:
        print(f"Error: {exc}")


def show_habit_streak():
    habits = list_habits(include_archived=True)
    if not habits:
        print("No habits found.")
        return
    for habit in habits:
        print(f"{habit['id']}. {habit['name']}")
    habit_id = safe_input("Enter habit ID: ")
    try:
        habit_id_int = int(habit_id)
    except ValueError:
        print("Invalid habit ID.")
        return

    try:
        summary = get_habit_streak_summary(habit_id_int)
        print(f"Habit: {summary['habit']['name']}")
        print(f"Current streak: {summary['current_streak']} days")
        print(f"Best streak: {summary['best_streak']} days")
    except ValueError as exc:
        print(f"Error: {exc}")


def search_habit_flow():
    term = safe_input("Search: ")
    if not term:
        print("Search term cannot be empty.")
        return
    results = search_habits_by_name(term)
    if not results:
        print("No matching habits found.")
        return
    for index, habit in enumerate(results, start=1):
        print(f"{index}. {habit['name']}")


def view_all_habits():
    habits = list_habits(include_archived=True)
    if not habits:
        print("No habits found.")
        return
    for habit in habits:
        status = "Archived" if habit["archived"] else "Active"
        print(f"{habit['id']}. {habit['name']} [{status}]")


def archive_habit_flow():
    habits = list_habits(include_archived=False)
    if not habits:
        print("No active habits to archive.")
        return
    for habit in habits:
        print(f"{habit['id']}. {habit['name']}")
    habit_id = safe_input("Enter habit ID to archive: ")
    try:
        archive_habit_record(int(habit_id))
        print("Habit archived successfully.")
    except (ValueError, TypeError):
        print("Invalid habit ID.")


def restore_habit_flow():
    habits = list_habits(include_archived=True)
    archived = [habit for habit in habits if habit["archived"]]
    if not archived:
        print("No archived habits found.")
        return
    for habit in archived:
        print(f"{habit['id']}. {habit['name']}")
    habit_id = safe_input("Enter habit ID to restore: ")
    try:
        restore_habit_record(int(habit_id))
        print("Habit restored successfully.")
    except (ValueError, TypeError):
        print("Invalid habit ID.")


def view_habit_history_flow():
    habits = list_habits(include_archived=True)
    if not habits:
        print("No habits found.")
        return
    for habit in habits:
        print(f"{habit['id']}. {habit['name']}")
    habit_id = safe_input("Enter habit ID: ")
    try:
        habit_id_int = int(habit_id)
    except ValueError:
        print("Invalid habit ID.")
        return

    try:
        history = get_habit_history(habit_id_int)
        habit_name = next(item["name"] for item in habits if item["id"] == habit_id_int)
        print(f"\nHabit: {habit_name}")
        for item in history:
            print(f"{item['date']}   {item['status']}")
    except ValueError as exc:
        print(f"Error: {exc}")


def view_challenge_progress():
    settings = get_challenge_settings()
    progress = get_challenge_progress(start_date=settings["start_date"], duration=settings["duration"])
    print("\n========================================")
    print("75-DAY CHALLENGE")
    print("========================================")
    print(f"Start Date: {progress['start_date']}")
    print(f"Today: {progress['today']}")
    print(f"Challenge Day: {progress['challenge_day']} / {progress['total_days']}")
    print(f"Remaining: {progress['remaining_days']} days")
    print(f"Progress: {progress['progress_percentage']}%")

    choice = safe_input("Update challenge start date? (y/n): ").lower()
    if choice == "y":
        new_start = safe_input("New start date (YYYY-MM-DD): ")
        try:
            update_challenge_start_date(new_start)
            print("Challenge start date updated.")
        except ValueError:
            print("Invalid date. Challenge start date was not changed.")


def import_price_list_flow():
    path = safe_input("CSV file path: ")
    if not path:
        print("File path cannot be empty.")
        return

    try:
        result = import_price_list_from_csv(path)
    except (OSError, ValueError) as exc:
        print(f"Error importing price list: {exc}")
        return

    print("\n========================================")
    print("SEAT-CLASS PRICE LIST IMPORT REPORT")
    print("========================================")
    print(f"Imported: {len(result['imported'])}")
    for item in result["imported"]:
        print(f"  {item['seat_class']}: {item['price']:.2f}")

    print(f"Deduplicated: {len(result['deduplicated'])}")
    for item in result["deduplicated"]:
        print(
            f"  {item['seat_class']}: {item['raw_price']!r} "
            f"({item['reason']})"
        )

    print(f"Rejected: {len(result['rejected'])}")
    for item in result["rejected"]:
        print(
            f"  {item['seat_class']}: {item['raw_price']!r} "
            f"({item['reason']})"
        )
    print("========================================")


def show_morning_reminder():
    from datetime import datetime

    current_time = datetime.now().time()
    if not (datetime.strptime("06:00", "%H:%M").time() <= current_time < datetime.strptime("12:00", "%H:%M").time()):
        return

    pending = get_pending_today_habits()
    print("\n========================================")
    print("       MORNING HABIT REMINDER")
    print("========================================")
    if not pending:
        today_habits = get_todays_habits()
        if not today_habits:
            print("No habits are scheduled for today.")
        else:
            print("Great! All scheduled habits for today are completed.")
        print("========================================")
        return

    if len(pending) == 1:
        print(f"Good morning! You still have {len(pending)} habit to complete today:")
    else:
        print(f"Good morning! You still have {len(pending)} habits to complete today:")
    for index, habit in enumerate(pending, start=1):
        print(f"{index}. {habit['name']}")
    print("\nComplete them from the main menu.")
    print("========================================")


def main():
    initialize_database()
    show_morning_reminder()
    while True:
        show_menu()
        choice = safe_input("Enter your choice: ")

        if choice == "1":
            show_todays_habits()
        elif choice == "2":
            add_habit_flow()
        elif choice == "3":
            update_habit_flow()
        elif choice == "4":
            complete_habit_flow()
        elif choice == "5":
            show_habit_streak()
        elif choice == "6":
            search_habit_flow()
        elif choice == "7":
            view_all_habits()
        elif choice == "8":
            archive_habit_flow()
        elif choice == "9":
            restore_habit_flow()
        elif choice == "10":
            view_habit_history_flow()
        elif choice == "11":
            view_challenge_progress()
        elif choice == "12":
            import_price_list_flow()
        elif choice == "13":
            print("Goodbye!")
            break
        else:
            print("Invalid menu choice. Please select a number from 1 to 13.")

        safe_input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()

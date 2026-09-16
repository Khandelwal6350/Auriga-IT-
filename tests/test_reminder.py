import unittest
from datetime import date

from database import add_completion, add_habit, get_connection
from habit_tracker.habit_manager import get_pending_today_habits


class ReminderTests(unittest.TestCase):
    def setUp(self):
        self.today = date.today().isoformat()
        self.habit_ids = []
        conn = get_connection()
        conn.execute("DELETE FROM completions")
        conn.execute("DELETE FROM habits")
        conn.execute("DELETE FROM sqlite_sequence WHERE name = 'habits'")
        conn.execute("DELETE FROM sqlite_sequence WHERE name = 'completions'")
        conn.commit()
        conn.close()

    def tearDown(self):
        conn = get_connection()
        conn.execute("DELETE FROM completions")
        conn.execute("DELETE FROM habits")
        conn.execute("DELETE FROM sqlite_sequence WHERE name = 'habits'")
        conn.execute("DELETE FROM sqlite_sequence WHERE name = 'completions'")
        conn.commit()
        conn.close()

    def add_test_habit(self, name, schedule_type='daily', schedule_days='', start_date=None, end_date=None, archived=0):
        if start_date is None:
            start_date = self.today
        habit_id = add_habit(name, name, schedule_type, schedule_days, start_date, end_date)
        self.habit_ids.append(habit_id)
        return habit_id

    def test_pending_daily_habit_appears(self):
        habit_id = self.add_test_habit('Drink Water')
        pending = get_pending_today_habits(self.today)
        self.assertIn(habit_id, [h['id'] for h in pending])

    def test_completed_today_habit_does_not_appear(self):
        habit_id = self.add_test_habit('Read Book')
        add_completion(habit_id, self.today)
        pending = get_pending_today_habits(self.today)
        self.assertNotIn(habit_id, [h['id'] for h in pending])

    def test_archived_habit_does_not_appear(self):
        habit_id = self.add_test_habit('Walk', archived=1)
        from database import get_connection
        conn = get_connection()
        conn.execute("UPDATE habits SET archived = 1 WHERE id = ?", (habit_id,))
        conn.commit()
        conn.close()
        pending = get_pending_today_habits(self.today)
        self.assertNotIn(habit_id, [h['id'] for h in pending])

    def test_non_scheduled_custom_habit_does_not_appear(self):
        non_schedule_date = date(2026, 9, 15).isoformat()  # Tuesday, not in Monday/Wednesday/Friday
        habit_id = self.add_test_habit(
            'Workout',
            schedule_type='custom',
            schedule_days='Monday, Wednesday, Friday',
            start_date=non_schedule_date,
        )
        pending = get_pending_today_habits(non_schedule_date)
        self.assertNotIn(habit_id, [h['id'] for h in pending])

    def test_future_start_habit_does_not_appear(self):
        future_date = date.today().fromordinal(date.today().toordinal() + 7).isoformat()
        habit_id = self.add_test_habit('Meditate', start_date=future_date)
        pending = get_pending_today_habits(self.today)
        self.assertNotIn(habit_id, [h['id'] for h in pending])

    def test_ended_habit_does_not_appear(self):
        past_date = date.today().fromordinal(date.today().toordinal() - 2).isoformat()
        habit_id = self.add_test_habit('Stretch', end_date=past_date)
        pending = get_pending_today_habits(self.today)
        self.assertNotIn(habit_id, [h['id'] for h in pending])

    def test_multiple_pending_habits_are_returned(self):
        habit_id_1 = self.add_test_habit('Drink Water')
        habit_id_2 = self.add_test_habit('Read Book')
        pending = get_pending_today_habits(self.today)
        ids = [h['id'] for h in pending]
        self.assertIn(habit_id_1, ids)
        self.assertIn(habit_id_2, ids)

    def test_no_pending_habits_returns_empty_result(self):
        conn = get_connection()
        conn.execute("DELETE FROM completions")
        conn.execute("DELETE FROM habits")
        conn.execute("DELETE FROM sqlite_sequence WHERE name = 'habits'")
        conn.execute("DELETE FROM sqlite_sequence WHERE name = 'completions'")
        conn.commit()
        conn.close()
        pending = get_pending_today_habits(self.today)
        self.assertEqual([], pending)

    def test_reminder_logic_does_not_create_duplicate_completions(self):
        habit_id = self.add_test_habit('Drink Water')
        add_completion(habit_id, self.today)
        result = add_completion(habit_id, self.today)
        self.assertFalse(result)
        pending = get_pending_today_habits(self.today)
        self.assertNotIn(habit_id, [h['id'] for h in pending])


if __name__ == '__main__':
    unittest.main()

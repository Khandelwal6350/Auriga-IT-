import unittest
from datetime import date, timedelta

from habit_tracker.streak import calculate_best_streak, calculate_current_streak


class StreakTests(unittest.TestCase):
    def make_habit(self, schedule_type, schedule_days=None, start_date='2026-01-01', end_date=None):
        return {
            'schedule_type': schedule_type,
            'schedule_days': schedule_days,
            'start_date': start_date,
            'end_date': end_date,
        }

    def test_daily_habit_streak(self):
        habit = self.make_habit('daily', start_date='2026-09-01', end_date='2026-09-05')
        completion_dates = {
            date(2026, 9, 1),
            date(2026, 9, 2),
            date(2026, 9, 3),
            date(2026, 9, 4),
            date(2026, 9, 5),
        }
        self.assertEqual(calculate_current_streak(habit, completion_dates), 5)
        self.assertEqual(calculate_best_streak(habit, completion_dates), 5)

    def test_weekday_streak(self):
        habit = self.make_habit('weekday', end_date='2026-09-11')
        completion_dates = {
            date(2026, 9, 7),
            date(2026, 9, 8),
            date(2026, 9, 9),
            date(2026, 9, 10),
            date(2026, 9, 11),
        }
        self.assertEqual(calculate_current_streak(habit, completion_dates), 5)

    def test_custom_schedule_streak(self):
        habit = self.make_habit('custom', schedule_days=['Monday', 'Wednesday', 'Friday'])
        completion_dates = {
            date(2026, 9, 7),
            date(2026, 9, 9),
            date(2026, 9, 11),
            date(2026, 9, 14),
            date(2026, 9, 16),
            date(2026, 9, 18),
        }
        self.assertEqual(calculate_current_streak(habit, completion_dates), 6)
        self.assertEqual(calculate_best_streak(habit, completion_dates), 6)

    def test_non_scheduled_days_do_not_break_streak(self):
        habit = self.make_habit('custom', schedule_days=['Monday', 'Wednesday', 'Friday'])
        completion_dates = {
            date(2026, 9, 7),
            date(2026, 9, 9),
            date(2026, 9, 11),
            date(2026, 9, 14),
            date(2026, 9, 16),
        }
        self.assertEqual(calculate_current_streak(habit, completion_dates), 5)

    def test_broken_streak_resets(self):
        habit = self.make_habit('daily', start_date='2026-09-01', end_date='2026-09-06')
        completion_dates = {
            date(2026, 9, 1),
            date(2026, 9, 2),
            date(2026, 9, 3),
            date(2026, 9, 5),
            date(2026, 9, 6),
        }
        self.assertEqual(calculate_current_streak(habit, completion_dates), 2)
        self.assertEqual(calculate_best_streak(habit, completion_dates), 3)

    def test_yesterday_missed_today_pending_breaks_streak(self):
        today = date.today()
        habit = self.make_habit('daily', start_date=today - timedelta(days=20))
        completion_dates = {
            today - timedelta(days=offset)
            for offset in range(2, 21)
        }

        self.assertEqual(calculate_current_streak(habit, completion_dates), 0)


if __name__ == '__main__':
    unittest.main()

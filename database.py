"""SQLite setup and helper queries for the habit tracker."""

import sqlite3
from datetime import date
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "habit_tracker.db"
DEFAULT_CHALLENGE_START = date.today().isoformat()


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()
    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                schedule_type TEXT NOT NULL,
                schedule_days TEXT,
                start_date TEXT NOT NULL,
                end_date TEXT,
                archived INTEGER DEFAULT 0,
                created_at TEXT NOT NULL
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS completions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                completion_date TEXT NOT NULL,
                completed_at TEXT NOT NULL,
                FOREIGN KEY(habit_id) REFERENCES habits(id),
                UNIQUE(habit_id, completion_date)
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS challenge (
                id INTEGER PRIMARY KEY,
                start_date TEXT NOT NULL,
                duration INTEGER DEFAULT 75
            )
            """
        )
        connection.execute(
            "INSERT OR IGNORE INTO challenge (id, start_date, duration) VALUES (1, ?, 75)",
            (DEFAULT_CHALLENGE_START,),
        )
        connection.commit()
    finally:
        connection.close()


def get_challenge_settings():
    connection = get_connection()
    try:
        row = connection.execute(
            "SELECT start_date, duration FROM challenge WHERE id = 1"
        ).fetchone()
        if row is None:
            return {"start_date": DEFAULT_CHALLENGE_START, "duration": 75}
        return {"start_date": row["start_date"], "duration": row["duration"]}
    finally:
        connection.close()


def update_challenge_start_date(start_date):
    connection = get_connection()
    try:
        connection.execute(
            "UPDATE challenge SET start_date = ? WHERE id = 1",
            (start_date,),
        )
        connection.commit()
    finally:
        connection.close()


def get_all_habits(include_archived=False):
    connection = get_connection()
    try:
        if include_archived:
            rows = connection.execute(
                "SELECT * FROM habits ORDER BY archived ASC, id ASC"
            ).fetchall()
        else:
            rows = connection.execute(
                "SELECT * FROM habits WHERE archived = 0 ORDER BY id ASC"
            ).fetchall()
        return [dict(row) for row in rows]
    finally:
        connection.close()


def get_habit_by_id(habit_id):
    connection = get_connection()
    try:
        row = connection.execute(
            "SELECT * FROM habits WHERE id = ?",
            (habit_id,),
        ).fetchone()
        if row is None:
            return None
        return dict(row)
    finally:
        connection.close()


def add_habit(name, description, schedule_type, schedule_days, start_date, end_date):
    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            INSERT INTO habits (name, description, schedule_type, schedule_days, start_date, end_date, archived, created_at)
            VALUES (?, ?, ?, ?, ?, ?, 0, datetime('now'))
            """,
            (name, description, schedule_type, schedule_days, start_date, end_date),
        )
        connection.commit()
        return cursor.lastrowid
    finally:
        connection.close()


def update_habit(habit_id, name, description, schedule_type, schedule_days, start_date, end_date):
    connection = get_connection()
    try:
        connection.execute(
            """
            UPDATE habits
            SET name = ?, description = ?, schedule_type = ?, schedule_days = ?, start_date = ?, end_date = ?
            WHERE id = ?
            """,
            (name, description, schedule_type, schedule_days, start_date, end_date, habit_id),
        )
        connection.commit()
    finally:
        connection.close()


def archive_habit(habit_id):
    connection = get_connection()
    try:
        connection.execute(
            "UPDATE habits SET archived = 1 WHERE id = ?",
            (habit_id,),
        )
        connection.commit()
    finally:
        connection.close()


def restore_habit(habit_id):
    connection = get_connection()
    try:
        connection.execute(
            "UPDATE habits SET archived = 0 WHERE id = ?",
            (habit_id,),
        )
        connection.commit()
    finally:
        connection.close()


def search_habits(name_query):
    connection = get_connection()
    try:
        rows = connection.execute(
            "SELECT * FROM habits WHERE lower(name) LIKE lower(?) AND archived = 0 ORDER BY id ASC",
            (f"%{name_query}%",),
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        connection.close()


def add_completion(habit_id, completion_date):
    connection = get_connection()
    try:
        connection.execute(
            "INSERT INTO completions (habit_id, completion_date, completed_at) VALUES (?, ?, datetime('now'))",
            (habit_id, completion_date),
        )
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        connection.close()


def get_completion_dates(habit_id):
    connection = get_connection()
    try:
        rows = connection.execute(
            "SELECT completion_date FROM completions WHERE habit_id = ? ORDER BY completion_date ASC",
            (habit_id,),
        ).fetchall()
        return [row["completion_date"] for row in rows]
    finally:
        connection.close()


def habit_is_completed_on_date(habit_id, completion_date):
    connection = get_connection()
    try:
        row = connection.execute(
            "SELECT 1 FROM completions WHERE habit_id = ? AND completion_date = ?",
            (habit_id, completion_date),
        ).fetchone()
        return row is not None
    finally:
        connection.close()

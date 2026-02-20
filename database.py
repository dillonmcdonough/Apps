"""
Database layer — wraps SQLite with a simple interface.
All SQL lives here; the rest of the app never touches it directly.
"""
import sqlite3
from pathlib import Path


class Database:
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = Path(__file__).parent / "torque_tracker.db"
        self.db_path = str(db_path)
        self._connect()
        self._create_tables()

    # ── connection ────────────────────────────────────────────────────────────

    def _connect(self):
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")

    def _create_tables(self):
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                username    TEXT UNIQUE NOT NULL,
                created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS vehicles (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id       INTEGER NOT NULL,
                name          TEXT    NOT NULL,
                make          TEXT    DEFAULT '',
                model         TEXT    DEFAULT '',
                year          INTEGER,
                license_plate TEXT    DEFAULT '',
                created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS mileage_logs (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                vehicle_id       INTEGER NOT NULL,
                odometer_reading REAL    NOT NULL,
                date             DATE    NOT NULL,
                notes            TEXT    DEFAULT '',
                created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE
            );
        """)
        self.conn.commit()

    # ── helpers ───────────────────────────────────────────────────────────────

    def execute(self, query: str, params: tuple = ()):
        """Run an INSERT / UPDATE / DELETE and commit."""
        cursor = self.conn.execute(query, params)
        self.conn.commit()
        return cursor

    def fetchall(self, query: str, params: tuple = ()):
        return self.conn.execute(query, params).fetchall()

    def fetchone(self, query: str, params: tuple = ()):
        return self.conn.execute(query, params).fetchone()

    def close(self):
        if self.conn:
            self.conn.close()

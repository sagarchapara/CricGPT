import os
import pathlib
import sqlite3
import logging
from datetime import datetime, timezone
from typing import Optional

logger = logging.getLogger(__name__)

class PersistentCache:
    def __init__(self, db_path: str = "cricgpt_cache.db"):
        try:
            self.db_path = os.path.realpath(os.path.expanduser(db_path))
            dir_path = os.path.dirname(self.db_path)

            if not os.path.exists(dir_path):
                pathlib.Path(dir_path).mkdir(parents=True, exist_ok=True, mode=0o755)

            if not os.path.exists(self.db_path):
                open(self.db_path, 'a').close()

            self.conn = sqlite3.connect(self.db_path)
            self._init_db()
        except sqlite3.OperationalError as e:
            logger.error(f"SQLite error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise

    def _connect(self):
        self.conn = sqlite3.connect(
            self.db_path,
            timeout=30,
            isolation_level=None
        )

    def _init_db(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cache (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    async def get(self, key: str) -> Optional[str]:
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT value FROM cache WHERE key = ?", (key,))
            row = cursor.fetchone()
            return row[0] if row else None
        except Exception as e:
            logger.error(f"Error getting key {key}: {e}")
            return None

    async def set(self, key: str, value: str) -> bool:
        try:
            cursor = self.conn.cursor()
            now = datetime.now(timezone.utc).isoformat()
            cursor.execute("""
                INSERT INTO cache (key, value, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(key) DO UPDATE
                SET value = excluded.value,
                    updated_at = excluded.updated_at
            """, (key, value, now))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error setting key {key}: {e}")
            return False

    async def delete(self, key: str) -> bool:
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM cache WHERE key = ?", (key,))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error deleting key {key}: {e}")
            return False

    def __del__(self):
        try:
            self.conn.close()
        except:
            pass
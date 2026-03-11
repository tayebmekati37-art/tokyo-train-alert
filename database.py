import sqlite3
import logging
from datetime import datetime

logger = logging.getLogger('TokyoTrainAlert')

class AlertDatabase:
    def __init__(self, db_path='alerts.db'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    line TEXT NOT NULL,
                    status TEXT NOT NULL,
                    message TEXT,
                    email_sent INTEGER DEFAULT 0
                )
            ''')
            conn.commit()

    def log_alert(self, line, status, message, email_sent=False):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO alerts (timestamp, line, status, message, email_sent)
                VALUES (?, ?, ?, ?, ?)
            ''', (datetime.now().isoformat(), line, status, message, 1 if email_sent else 0))
            conn.commit()
            logger.debug("Alert logged to database.")
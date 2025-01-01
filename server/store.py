from dataclasses import dataclass
import psycopg2
import sqlite3
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional
import os, time, json, logging
from dotenv import load_dotenv
from utils.utils import datetime_to_epoch

logger = logging.getLogger(__name__)

@dataclass
class Session:
    id: str
    messages: List[Dict]
    sharedLink: str
    lastUpdated: int = datetime_to_epoch(datetime.now(timezone.utc))
    numMessages: int = 0
    numLikes: int = 0
    numDislikes: int = 0


class SessionStore:
    def __init__(self):

        load_dotenv()

        dbname = os.getenv("DB_NAME")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")

        self.conn_params = {
            "dbname": dbname,
            "user": user,
            "password": password,
            "host": host,
            "port": port
        }
        self._create_table()

    def _get_connection(self):
        return psycopg2.connect(**self.conn_params)

    def _create_table(self):
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS sessions (
                        session_id VARCHAR(255) PRIMARY KEY,
                        messages JSONB,
                        shared_link VARCHAR(255),
                        last_updated TIMESTAMP,
                        num_messages INTEGER DEFAULT 0,
                        num_likes INTEGER DEFAULT 0,
                        num_dislikes INTEGER DEFAULT 0
                    )
                """)

    def upsert_multiple(self, sessions: List[Session]) -> None:
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.executemany("""
                    INSERT INTO sessions (session_id, messages, shared_link, last_updated, num_messages, num_likes, num_dislikes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (session_id) DO UPDATE SET
                        messages = EXCLUDED.messages,
                        shared_link = EXCLUDED.shared_link,
                        last_updated = EXCLUDED.last_updated,
                        num_messages = EXCLUDED.num_messages,
                        num_likes = EXCLUDED.num_likes,
                        num_dislikes = EXCLUDED.num_dislikes
                """, [(session.id, json.dumps(session.messages), session.sharedLink, session.lastUpdated, session.numMessages, session.numLikes, session.numDislikes) for session in sessions])


    def upsert(self, session: Session) -> None:
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO sessions (session_id, messages, shared_link, last_updated, num_messages, num_likes, num_dislikes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (session_id) DO UPDATE SET
                        messages = EXCLUDED.messages,
                        shared_link = EXCLUDED.shared_link,
                        last_updated = EXCLUDED.last_updated,
                        num_messages = EXCLUDED.num_messages,
                        num_likes = EXCLUDED.num_likes,
                        num_dislikes = EXCLUDED.num_dislikes
                """, (session.id, json.dumps(session.messages), session.sharedLink, session.lastUpdated, session.numMessages, session.numLikes, session.numDislikes))



    def get(self, session_id: str) -> Optional[Session]:
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT messages, shared_link, last_updated, num_messages, num_likes, num_dislikes
                    FROM sessions
                    WHERE session_id = %s
                """, (session_id,))
                row = cur.fetchone()
                if not row:
                    return None
                messages, shared_link, last_updated, num_messages, num_likes, num_dislikes = row
                return Session(
                    id=session_id,
                    messages=json.loads(messages),
                    sharedLink=shared_link,
                    lastUpdated=last_updated,
                    numMessages=num_messages,
                    numLikes=num_likes,
                    numDislikes=num_dislikes
                )


class LocalSessionStore:
    def __init__(self, db_path='sessions.db'):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    messages TEXT,
                    shared_link TEXT,
                    last_updated INTEGER,
                    num_messages INTEGER DEFAULT 0,
                    num_likes INTEGER DEFAULT 0,
                    num_dislikes INTEGER DEFAULT 0
                )
            ''')

    def get(self, session_id: str) -> Optional[Session]:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute(
                'SELECT messages, shared_link, last_updated, num_messages, num_likes, num_dislikes FROM sessions WHERE session_id = ?',
                (session_id,)
            )
            row = cur.fetchone()
            if not row:
                return None
            
            messages, shared_link, last_updated, num_messages, num_likes, num_dislikes = row
            return Session(
                id=session_id,
                messages=json.loads(messages),
                sharedLink=shared_link,
                lastUpdated=last_updated,
                numMessages=num_messages,
                numLikes=num_likes,
                numDislikes=num_dislikes
            )

    
    
    def upsert(self, session: Session):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
            '''
            INSERT INTO sessions (session_id, messages, shared_link, last_updated, num_messages, num_likes, num_dislikes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(session_id) DO UPDATE SET
                messages = excluded.messages,
                shared_link = excluded.shared_link,
                last_updated = excluded.last_updated,
                num_messages = excluded.num_messages,
                num_likes = excluded.num_likes,
                num_dislikes = excluded.num_dislikes
            WHERE excluded.last_updated > sessions.last_updated
            ''',
            (session.id, json.dumps(session.messages), session.sharedLink, session.lastUpdated, session.numMessages, session.numLikes, session.numDislikes)
            )

    def get_sessions(self, last_updated: int) -> List[Session]:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute(
                'SELECT session_id, messages, shared_link, last_updated, num_messages, num_likes, num_dislikes FROM sessions WHERE last_updated > ?',
                (last_updated,)
            )
            rows = cur.fetchall()
            return [
                Session(
                    id=row[0],
                    messages=json.loads(row[1]),
                    sharedLink=row[2],
                    lastUpdated=row[3],
                    numMessages=row[4],
                    numLikes=row[5],
                    numDislikes=row[6]
                )
                for row in rows
            ]
        
    def delete(self, sessionIds: list[str]):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                'DELETE FROM sessions WHERE session_id IN ({})'.format(','.join('?' * len(sessionIds))),
                sessionIds
            )

    

class SessionCronJob:
    def __init__(self, localstore: LocalSessionStore, sessionstore: SessionStore):
        self.localstore = localstore
        self.sessionstore = sessionstore

    def push_to_remote(self):

        try:
            # get all the sessions with last updated time > 10mins
            last_updated = int((datetime.now() - timedelta(minutes=10)).timestamp())

            sessions = self.localstore.get_sessions(last_updated)

            # upsert these sessions to the remote store
            self.sessionstore.upsert_multiple(sessions)

            # delete these sessions from the local store
            sessionIds = [session.id for session in sessions]
            self.localstore.delete(sessionIds)

            logger.info(f"Pushed {len(sessions)} sessions to remote store")

        except Exception as e:
            logger.error(f"Error pushing to remote store: {e}")
        

    def run(self):
        while True:
            self.push_to_remote()
            # sleep for 5 mins
            time.sleep(300)


        






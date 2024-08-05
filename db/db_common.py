import sqlite3

from config.config import Config
from db import db_history_of_users_tasks, db_users_utc_offset


def get_connection() -> sqlite3.Connection:
    con = sqlite3.connect(
        Config().databases.database, detect_types=sqlite3.PARSE_DECLTYPES
    )
    con.row_factory = sqlite3.Row
    return con


def init(db_conn: sqlite3.Connection):
    db_history_of_users_tasks.init(db_conn)
    db_users_utc_offset.init(db_conn)

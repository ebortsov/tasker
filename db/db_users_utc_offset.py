import sqlite3
from datetime import timedelta

from constants.utc_offsets import UTCOffset

CREATE_TABLE = """CREATE TABLE IF NOT EXISTS users_utc_offset (
    telegram_user_id INTEGER UNIQUE PRIMARY KEY,
    utc_offset UTC_OFFSET
)"""
UPDATE_USER_UTC_OFFSET = """INSERT OR REPLACE INTO users_utc_offset VALUES (?, ?)"""
SELECT_USER = """SELECT * FROM users_utc_offset WHERE telegram_user_id = ?"""


def offset_adapter(offset: UTCOffset) -> str:
    # Adapter of UTCOffset class to sqlite-supported type
    return f"{'-' if offset.sign < 0 else ''}{offset.hours:02}:{offset.minutes:02}"


def converter_to_offset(record: bytes) -> UTCOffset:
    # Convert SQl type to UTCOffset
    hours = abs(int(record.split(b":")[0]))
    minutes = int(record.split(b":")[1])
    sign = -1 if record[0] == b"-" else (1 if hours or minutes else 0)
    return UTCOffset(hours=hours, minutes=minutes, sign=sign)


def create_table(db_conn: sqlite3.Connection):
    with db_conn:
        db_conn.execute(CREATE_TABLE)


def init(db_conn: sqlite3.Connection):
    create_table(db_conn)
    sqlite3.register_adapter(UTCOffset, offset_adapter)
    sqlite3.register_converter("UTC_OFFSET", converter_to_offset)


def update_utc_offset(db_conn: sqlite3.Connection, user_id: int, utc_offset: UTCOffset):
    with db_conn:
        db_conn.execute(UPDATE_USER_UTC_OFFSET, (user_id, utc_offset))


def get_user_utc_offset(db_conn: sqlite3.Connection, user_id: int):
    with db_conn:
        result = db_conn.execute(SELECT_USER, (user_id,)).fetchone()
        return result["utc_offset"] if result else UTCOffset(hours=0, minutes=0, sign=0)


def get_user_utc_offset_as_timedelta(
    db_conn: sqlite3.Connection, user_id: int
) -> timedelta:
    result = get_user_utc_offset(db_conn, user_id)
    return timedelta(
        hours=result.hours * result.sign, minutes=result.minutes * result.sign
    )

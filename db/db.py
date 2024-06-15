import sqlite3
from config.config import Config
from task.task import Task

CREATE_TABLE = """CREATE TABLE IF NOT EXISTS history_of_users_tasks (
    telegram_user_id INTEGER NOT NULL,
    task_name TEXT NOT NULL,
    task_description TEXT NOT NULL
)"""
SAVE_TASK = """INSERT INTO history_of_users_tasks VALUES (?, ?, ?)"""
GET_ALL_COMPLETED_TASK = """SELECT rowid, * FROM history_of_users_tasks WHERE telegram_user_id = ?"""
EDIT_TASK_NAME = """
UPDATE history_of_users_tasks 
SET task_name = ? 
WHERE rowid = ? AND telegram_user_id = ?
"""
EDIT_TASK_DESCRIPTION = """
UPDATE history_of_users_tasks 
SET task_description = ? 
WHERE rowid = ? AND telegram_user_id = ?
"""
DELETE_TASK = """DELETE FROM history_of_users_tasks WHERE rowid = ? AND telegram_user_id = ?"""
SELECT_TASK_BY_ID = """SELECT rowid, * FROM history_of_users_tasks WHERE rowid = ? AND telegram_user_id = ?"""


def get_connection() -> sqlite3.Connection:
    con = sqlite3.connect(Config().databases.database)
    con.row_factory = sqlite3.Row
    return con


def create_table(db_conn: sqlite3.Connection):
    with db_conn:
        db_conn.execute(CREATE_TABLE)


def save_task(db_conn: sqlite3.Connection, task: Task):
    with db_conn:
        db_conn.execute(SAVE_TASK, (task.user_id, task.name, task.desc))


def get_all_completed_tasks(db_conn: sqlite3.Connection, user_id: int) -> list[Task]:
    with db_conn:
        res = db_conn.execute(GET_ALL_COMPLETED_TASK, (user_id,)).fetchall()
        return [
            Task(
                task_id=item['rowid'],
                user_id=item['telegram_user_id'],
                name=item['task_name'],
                desc=item['task_description']
            )
            for item in res
        ]


def edit_task_name(
        db_conn: sqlite3.Connection,
        new_task_name: str,
        task_id: int,
        user_id: int,
) -> None:
    with db_conn:
        db_conn.execute(EDIT_TASK_NAME, (new_task_name, task_id, user_id))


def edit_task_description(
        db_conn: sqlite3.Connection,
        new_task_description: str,
        task_id: int,
        user_id: int
) -> None:
    with db_conn:
        db_conn.execute(EDIT_TASK_DESCRIPTION, (new_task_description, task_id, user_id))


def delete_task(
        db_conn: sqlite3.Connection,
        task_id: int,
        user_id: int
) -> None:
    with db_conn:
        db_conn.execute(DELETE_TASK, (task_id, user_id))


def get_task(
        db_conn: sqlite3.Connection,
        task_id: str | int,
        user_id: int
) -> Task | None:
    with db_conn:
        result = db_conn.execute(SELECT_TASK_BY_ID, (task_id, user_id)).fetchone()
        if result is None:
            return None
        return Task(
            task_id=result['rowid'],
            user_id=result['telegram_user_id'],
            name=result['task_name'],
            desc=result['task_description']
        )

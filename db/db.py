import sqlite3
from config.config import Config
from task.task import Task

CREATE_TABLE = """CREATE TABLE IF NOT EXISTS history_of_users_tasks (
    telegram_user_id INTEGER NOT NULL,
    task_name TEXT NOT NULL,
    task_description TEXT NOT NULL
)"""
SAVE_TASK = """INSERT INTO history_of_users_tasks VALUES (?, ?, ?)"""
GET_ALL_COMPLETED_TASK = """SELECT * FROM history_of_users_tasks WHERE telegram_user_id = ?"""


def get_connection() -> sqlite3.Connection:
    con = sqlite3.connect(Config().databases.history_of_users_tasks)
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
                user_id=item['telegram_user_id'],
                name=item['task_name'],
                desc=item['task_description']
            )
            for item in res
        ]

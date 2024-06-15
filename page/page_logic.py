from db import db_history_of_users_tasks
from sqlite3 import Connection
from task.task import Task
from lexicon.simple_lexicion import DefaultLexicon
from constants.constants import MAX_PAGE_LENGTH
from page.page import Page

from typing import Optional
import logging


# Split the tasks greedily starting from the oldest ones
# By writing 'greedily' I mean that we add tasks to the current page
# until the length of the page does not exceed 4096 symbols

# If the last_page parameter is passed, then the page_num parameter is ignored
def get_page(
        db_conn: Connection,
        user_id: int,
        lexicon: DefaultLexicon,
        page_num: Optional[int] = None,
        last_page: Optional[bool] = None
) -> Page:
    completed_tasks: list[Task] = db.get_all_completed_tasks(db_conn, user_id)

    current_page = 1
    accumulated_length = 0
    result: list[Task] = []

    for task in completed_tasks:
        task_length = len(lexicon.form_task(task))

        if accumulated_length + task_length > MAX_PAGE_LENGTH:
            if current_page == page_num:
                break
            current_page += 1
            accumulated_length = 0
            result = []

        accumulated_length += task_length
        if current_page == page_num or last_page:
            result.append(task)

    logging.debug(accumulated_length)
    return Page(
        page_num=current_page,
        is_last_page=result and result[-1] is completed_tasks[-1],
        tasks=result
    )

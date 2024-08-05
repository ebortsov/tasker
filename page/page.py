from dataclasses import dataclass

from task.task import Task


class NoPage(Exception):
    def __init__(self, message: str):
        super().__init__(message)


@dataclass
class Page:
    page_num: int
    is_last_page: bool
    tasks: list[Task]

from dataclasses import dataclass
from typing import Optional
from datetime import timedelta
from datetime import datetime


@dataclass
class Task:
    user_id: int
    task_id: Optional[int] = None
    name: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    desc: Optional[str] = None

    def get_duration(self) -> timedelta:
        return self.end_time - self.start_time

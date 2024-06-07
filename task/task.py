from dataclasses import dataclass
from typing import Optional
from datetime import timedelta


@dataclass
class Task:
    user_id: int
    name: Optional[str] = None
    start_time_timestamp_seconds: Optional[int] = None
    end_time_timestamp_seconds: Optional[int] = None
    desc: Optional[str] = None

    def get_duration(self) -> timedelta:
        return timedelta(seconds=self.end_time_timestamp_seconds - self.start_time_timestamp_seconds)

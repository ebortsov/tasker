# utc_offset.py

from dataclasses import dataclass
from typing import List


@dataclass
class UTCOffset:
    hours: int
    minutes: int
    sign: int


UTC_OFFSETS: List[UTCOffset] = [
    UTCOffset(hours=12, minutes=0, sign=-1),
    UTCOffset(hours=11, minutes=0, sign=-1),
    UTCOffset(hours=10, minutes=0, sign=-1),
    UTCOffset(hours=9, minutes=30, sign=-1),
    UTCOffset(hours=9, minutes=0, sign=-1),
    UTCOffset(hours=8, minutes=0, sign=-1),
    UTCOffset(hours=7, minutes=0, sign=-1),
    UTCOffset(hours=6, minutes=0, sign=-1),
    UTCOffset(hours=5, minutes=0, sign=-1),
    UTCOffset(hours=4, minutes=0, sign=-1),
    UTCOffset(hours=3, minutes=30, sign=-1),
    UTCOffset(hours=3, minutes=0, sign=-1),
    UTCOffset(hours=2, minutes=0, sign=-1),
    UTCOffset(hours=1, minutes=0, sign=-1),
    UTCOffset(hours=0, minutes=0, sign=0),
    UTCOffset(hours=1, minutes=0, sign=1),
    UTCOffset(hours=2, minutes=0, sign=1),
    UTCOffset(hours=3, minutes=0, sign=1),
    UTCOffset(hours=3, minutes=30, sign=1),
    UTCOffset(hours=4, minutes=0, sign=1),
    UTCOffset(hours=4, minutes=30, sign=1),
    UTCOffset(hours=5, minutes=0, sign=1),
    UTCOffset(hours=5, minutes=30, sign=1),
    UTCOffset(hours=5, minutes=45, sign=1),
    UTCOffset(hours=6, minutes=0, sign=1),
    UTCOffset(hours=6, minutes=30, sign=1),
    UTCOffset(hours=7, minutes=0, sign=1),
    UTCOffset(hours=8, minutes=0, sign=1),
    UTCOffset(hours=8, minutes=45, sign=1),
    UTCOffset(hours=9, minutes=0, sign=1),
    UTCOffset(hours=9, minutes=30, sign=1),
    UTCOffset(hours=10, minutes=0, sign=1),
    UTCOffset(hours=10, minutes=30, sign=1),
    UTCOffset(hours=11, minutes=0, sign=1),
    UTCOffset(hours=12, minutes=0, sign=1),
    UTCOffset(hours=12, minutes=45, sign=1),
    UTCOffset(hours=13, minutes=0, sign=1),
    UTCOffset(hours=14, minutes=0, sign=1)
]

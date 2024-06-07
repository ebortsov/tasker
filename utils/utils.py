from datetime import timedelta


def hours_minutes_from_timedelta(duration: timedelta) -> tuple[int, int]:
    hours = duration.days * 24 + duration.seconds // 3600
    minutes = duration.seconds % 3600 // 60
    return hours, minutes

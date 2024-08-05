from aiogram.filters.callback_data import CallbackData


class UTCOffsetCallbackData(CallbackData, prefix="utf_offset"):
    offset_hours: int
    offset_minutes: int
    offset_sign: int

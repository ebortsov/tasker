from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from constants.utc_offsets import UTC_OFFSETS
from handlers.utc_offset_update.callback_data import UTCOffsetCallbackData


def get_update_utc_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    keyboard_width = 6
    builder_row = [
        InlineKeyboardButton(
            text=f"{'-' if offset.sign < 0 else ''}{offset.hours:02}:{offset.minutes:02}",
            callback_data=UTCOffsetCallbackData(
                offset_hours=offset.hours,
                offset_minutes=offset.minutes,
                offset_sign=offset.sign,
            ).pack(),
        )
        for offset in UTC_OFFSETS
    ]

    # Add some additional buttons so that markup looks good
    while len(builder_row) % keyboard_width:
        builder_row.append(InlineKeyboardButton(text='-', callback_data='.'))

    builder.row(*builder_row, width=keyboard_width)
    return builder.as_markup()

from aiogram import Router
from aiogram.types import CallbackQuery

from lexicon.simple_lexicion import DefaultLexicon
from handlers.utc_offset_update.callback_data import UTCOffsetCallbackData
from db import db_users_utc_offset
from constants.utc_offsets import UTCOffset

import sqlite3
import logging


router = Router()


@router.callback_query(UTCOffsetCallbackData.filter())
async def set_utc_offset(
        callback_query: CallbackQuery,
        lexicon: DefaultLexicon,
        db_conn: sqlite3.Connection,
        callback_data: UTCOffsetCallbackData
):
    try:
        db_users_utc_offset.update_utc_offset(
            db_conn=db_conn,
            user_id=callback_query.from_user.id,
            utc_offset=UTCOffset(
                hours=callback_data.offset_hours,
                minutes=callback_data.offset_minutes,
                sign=callback_data.offset_sign
            )
        )
        await callback_query.message.edit_text(text=lexicon.msg_utc_offset_updated)
    except Exception as e:
        logging.error(e)

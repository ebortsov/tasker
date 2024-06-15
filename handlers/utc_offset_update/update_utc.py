from aiogram import Router
from aiogram.types import CallbackQuery

from lexicon.simple_lexicion import DefaultLexicon
import sqlite3
from handlers.utc_offset_update.callback_data import UTCOffsetCallbackData
import logging

router = Router()


@router.callback_query(UTCOffsetCallbackData.filter())
async def set_utc_offset(
        callback_query: CallbackQuery,
        lexicon: DefaultLexicon,
        db_conn: sqlite3.Connection
):
    # Store offset in the database...
    try:
        await callback_query.message.edit_text(text=lexicon.msg_utc_offset_updated)
    except Exception as e:
        logging.error(e)

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.types import Message

from lexicon.simple_lexicion import DefaultLexicon
from states.states import TaskCreationStates
import sqlite3
from page.page_logic import get_page
from page.page import Page
from keyboards import pagination_keyboards
from handlers.pagination.callback_data import SwitchPageCallback

router = Router()


@router.message(
    lambda message, lexicon: message.text == lexicon.kb_show_prev_tasks,
    TaskCreationStates.main_menu
)
async def show_completed_tasks(
        message: Message,
        db_conn: sqlite3.Connection,
        lexicon: DefaultLexicon
):
    page: Page = get_page(db_conn, message.from_user.id, lexicon, last_page=True)
    if not page.tasks:
        # User has not completed any tasks yet
        await message.answer(lexicon.msg_no_completed_tasks)
        return

    await message.answer(
        text=''.join(map(lexicon.form_task, page.tasks)),
        reply_markup=pagination_keyboards.get_corresponding_keyboard(page, lexicon)
    )


@router.callback_query(SwitchPageCallback.filter())
async def show_page(
        callback: CallbackQuery,
        db_conn: sqlite3.Connection,
        lexicon: DefaultLexicon,
        callback_data: SwitchPageCallback,
):
    page: Page = get_page(db_conn, callback.from_user.id, lexicon, callback_data.page_num)
    if page.tasks:
        # Such page exists
        await callback.message.edit_text(
            text=''.join(map(lexicon.form_task, page.tasks)),
            reply_markup=pagination_keyboards.get_corresponding_keyboard(page, lexicon)
        )
        await callback.answer()

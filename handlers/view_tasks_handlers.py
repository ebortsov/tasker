from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from lexicon.simple_lexicion import DefaultLexicon
from db import db
from task.task import Task
from states.states import TaskCreationStates
import sqlite3

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
    completed_tasks = db.get_all_completed_tasks(db_conn, message.from_user.id)
    if not completed_tasks:
        # User has not completed any tasks yet
        await message.answer(lexicon.msg_no_completed_tasks)
        return

    await message.answer(lexicon.form_completed_tasks(completed_tasks))

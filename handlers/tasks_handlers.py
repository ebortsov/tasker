from aiogram import Router
from aiogram.types import Message
from aiogram.types import ReplyKeyboardRemove
from aiogram import html
from aiogram import F
from aiogram.fsm.context import FSMContext
from states.states import TaskCreationStates
from aiogram.filters import and_f, or_f
from datetime import timedelta

import time
from math import floor
import sqlite3

from lexicon.simple_lexicion import DefaultLexicon
from keyboards import keyboards
from keyboards import update_utc_keyboard
from task.task import Task
from utils.utils import hours_minutes_from_timedelta
from db import db_history_of_users_tasks
from db import db_users_utc_offset
from constants import constants

router = Router()


@router.message(
    lambda message, lexicon: message.text == lexicon.kb_start_new_task,
    TaskCreationStates.main_menu
)
async def start_new_task(message: Message, state: FSMContext, lexicon: DefaultLexicon):
    # User wants to start the new task
    # Prompt the user to enter the name of the new task
    await message.answer(
        text=lexicon.msg_new_task_name_enter_prompt,
        reply_markup=keyboards.get_cancel_kb(lexicon)
    )
    # Switch the state
    await state.set_state(TaskCreationStates.new_task_name_enter)


@router.message(
    lambda message, lexicon: message.text == lexicon.kb_update_utc_offset,
    TaskCreationStates.main_menu
)
async def update_utc_offset(message: Message, lexicon: DefaultLexicon):
    await message.answer(
        text=lexicon.msg_select_utc_offset,
        reply_markup=update_utc_keyboard.get_update_utc_keyboard()
    )


@router.message(
    lambda message, lexicon: message.text == lexicon.kb_cancel_task_creation,
    TaskCreationStates.new_task_name_enter
)
async def new_task_name_enter_cancel(message: Message, state: FSMContext, lexicon: DefaultLexicon):
    # User wants to cancel the start of the new task
    await message.answer(
        text=lexicon.msg_new_task_cancelled,
        reply_markup=keyboards.get_start_kb(lexicon)
    )
    # Switch the state
    await state.set_state(TaskCreationStates.main_menu)


@router.message(TaskCreationStates.new_task_name_enter)
async def new_task_name_enter(
        message: Message,
        state: FSMContext,
        lexicon: DefaultLexicon,
        db_conn: sqlite3.Connection
):
    # User entered the name of the task. Now we need to start the new task

    # But before that we need to check that the name of the task does not exceed 256 characters
    # (needed for pagination purposes)
    task_name = message.text
    if len(task_name) > constants.MAX_TASK_NAME_LENGTH:
        await message.answer(
            lexicon.msg_too_long_task_name.format(
                max_task_name_length=constants.MAX_TASK_NAME_LENGTH
            )
        )
        return

    user_offset = db_users_utc_offset.get_user_utc_offset_as_timedelta(db_conn, message.from_user.id)

    # Remember the name and the start time of the task
    await state.update_data(
        task=Task(
            user_id=message.from_user.id,
            name=task_name,
            start_time=message.date + user_offset
        )
    )

    await message.answer(
        text=lexicon.msg_ongoing_task_start.format(task_name=html.quote(task_name)),
        reply_markup=keyboards.get_ongoing_task_kb(lexicon)
    )

    # Switch the state
    await state.set_state(TaskCreationStates.ongoing_task)


@router.message(
    lambda message, lexicon: message.text == lexicon.kb_cancel_ongoing_task,
    TaskCreationStates.ongoing_task
)
async def cancel_ongoing_task_confirm(message: Message, state: FSMContext, lexicon: DefaultLexicon):
    # User wants to cancel the ongoing task
    # In this handler we want to receive confirmation in task cancellation
    await message.answer(
        text=lexicon.msg_cancel_ongoing_task_confirm,
        reply_markup=keyboards.get_cancel_ongoing_task_confirm_kb(lexicon)
    )
    await state.set_state(TaskCreationStates.ongoing_task_cancel_confirm)


@router.message(
    lambda message, lexicon: message.text == lexicon.kb_cancel_ongoing_task_confirm,
    TaskCreationStates.ongoing_task_cancel_confirm
)
async def kill_task(message: Message, state: FSMContext, lexicon: DefaultLexicon):
    # User confirms that they want to cancel the task
    current_task: Task = (await state.get_data())['task']
    await message.answer(
        text=lexicon.msg_task_killed.format(task_name=current_task.name),
        reply_markup=keyboards.get_start_kb(lexicon)
    )

    # Clear the state data and return to the main menu
    await state.set_data({})
    await state.set_state(TaskCreationStates.main_menu)


@router.message(
    and_f(
        lambda message, lexicon: message.text == lexicon.kb_continue_ongoing_task,
        or_f(TaskCreationStates.ongoing_task_cancel_confirm, TaskCreationStates.finish_ongoing_task_confirm)
    )
)
async def continue_task(message: Message, state: FSMContext, lexicon: DefaultLexicon):
    # User wants to continue the task (applies to both cancellation and finalization of the task)
    current_task: Task = (await state.get_data())['task']
    await message.answer(
        text=lexicon.msg_continue_task.format(task_name=current_task.name),
        reply_markup=keyboards.get_ongoing_task_kb(lexicon)
    )
    await state.set_state(TaskCreationStates.ongoing_task)


@router.message(
    lambda message, lexicon: message.text == lexicon.kb_finish_ongoing_task,
    TaskCreationStates.ongoing_task
)
async def finish_task_confirm(message: Message, state: FSMContext, lexicon: DefaultLexicon):
    # User wants to finish current task
    current_task: Task = (await state.get_data())['task']
    await message.answer(
        text=lexicon.msg_finish_ongoing_task_confirm.format(task_name=current_task.name),
        reply_markup=keyboards.get_finish_task_confirm_kb(lexicon)
    )
    await state.set_state(TaskCreationStates.finish_ongoing_task_confirm)


@router.message(
    lambda message, lexicon: message.text == lexicon.kb_finish_ongoing_task_confirm,
    TaskCreationStates.finish_ongoing_task_confirm
)
async def finish_task(message: Message, state: FSMContext, lexicon: DefaultLexicon):
    await message.answer(
        text=lexicon.msg_enter_task_description,
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(TaskCreationStates.completed_task_desc_enter)


@router.message(F.text, TaskCreationStates.completed_task_desc_enter)
async def enter_description(
        message: Message,
        state: FSMContext,
        lexicon: DefaultLexicon,
        db_conn: sqlite3.Connection
):
    # The length of the description must not exceed 2048 utf-8 characters (needed for task preview pagination)
    task_description = message.text
    if len(task_description) > constants.MAX_TASK_DESCRIPTION_LENGTH:
        await message.answer(
            lexicon.msg_too_long_description.format(
                max_task_description_length=constants.MAX_TASK_DESCRIPTION_LENGTH
            )
        )
        return

    current_task: Task = (await state.get_data())['task']

    user_offset = db_users_utc_offset.get_user_utc_offset_as_timedelta(db_conn, message.from_user.id)
    current_task.end_time = message.date + user_offset
    current_task.desc = message.text

    # Saving data to the database
    db_history_of_users_tasks.save_task(db_conn, current_task)

    hours, minutes = hours_minutes_from_timedelta(current_task.get_duration())

    await message.answer(
        text=lexicon.msg_task_completed.format(task_name=current_task.name, hours=hours, minutes=minutes),
        reply_markup=keyboards.get_start_kb(lexicon)
    )

    await state.set_data({})
    await state.set_state(TaskCreationStates.main_menu)

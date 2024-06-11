"""
This module contains handlers related to editing of the tasks. To edit the task, user must enter the command in the following format:
/edit_task_{task_id}
where task_id is a rowid attribute of a task record in the database
See form_completed_tasks() in module simple_lexicon.py to know how user enters these commands
"""
from aiogram import Router
from aiogram.types import Message
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram import F

from lexicon.simple_lexicion import DefaultLexicon
from keyboards import keyboards
from states.states import TaskEditStates
from states.states import TaskCreationStates
from db import db
from handlers import constants
from task.task import Task

import sqlite3

router = Router()


@router.message(
    lambda message: message.text.startswith('/edit_task'),
    TaskCreationStates.main_menu,
)
async def show_task_edit_menu(
        message: Message,
        state: FSMContext,
        db_conn: sqlite3.Connection,
        lexicon: DefaultLexicon,
):
    task_id = int(message.text.split('_', maxsplit=3)[-1])
    task = db.get_task(db_conn, task_id, message.from_user.id)
    if task is None:
        await message.answer(lexicon.msg_no_such_task)
        return

    await message.answer(
        text=lexicon.msg_show_edit_task_menu,
        reply_markup=keyboards.get_task_edit_kb(lexicon)
    )

    await state.update_data(task=task)
    await state.set_state(TaskEditStates.menu)


@router.message(
    lambda message, lexicon: message.text == lexicon.kb_back_to_main_menu_from_edit_menu,
    TaskEditStates.menu
)
async def back_to_main_menu(message: Message, state: FSMContext, lexicon: DefaultLexicon):
    await message.answer(
        text=lexicon.msg_cancel_task_edit,
        reply_markup=keyboards.get_start_kb(lexicon)
    )
    # Return to the main keyboard
    await state.set_state(TaskCreationStates.main_menu)
    # Clear the data
    await state.set_data({})


@router.message(
    lambda message, lexicon: message.text == lexicon.kb_edit_task_name,
    TaskEditStates.menu
)
async def edit_task_name_enter(
        message: Message,
        state: FSMContext,
        lexicon: DefaultLexicon,
):
    await message.answer(
        text=lexicon.msg_edit_task_name,
        reply_markup=ReplyKeyboardRemove()
    )

    # Change the state
    await state.set_state(TaskEditStates.edit_task_name)


@router.message(F.text, TaskEditStates.edit_task_name)
async def edit_name(
        message: Message,
        state: FSMContext,
        db_conn: sqlite3,
        lexicon: DefaultLexicon
):
    new_task_name = message.text
    # Task name is too long
    if len(new_task_name) > constants.MAX_TASK_NAME_LENGTH:
        await message.answer(
            lexicon.msg_too_long_task_name.format(
                max_task_name_length=constants.MAX_TASK_NAME_LENGTH
            )
        )
        return

    task: Task = (await state.get_data())['task']

    # Edit the name of the task with the provided task_id
    db.edit_task_name(db_conn, new_task_name, task.task_id, task.user_id)
    await message.answer(
        lexicon.msg_task_name_edited,
        reply_markup=keyboards.get_task_edit_kb(lexicon)
    )
    # And just return to the edit keyboard
    await state.set_state(TaskEditStates.menu)


# Yeah... I know it basically a code repetition...
@router.message(
    lambda message, lexicon: message.text == lexicon.kb_edit_task_description,
    TaskEditStates.menu
)
async def edit_task_description(
        message: Message,
        state: FSMContext,
        lexicon: DefaultLexicon,
):
    await message.answer(
        text=lexicon.msg_edit_task_description,
        reply_markup=ReplyKeyboardRemove()
    )

    # Change the state
    await state.set_state(TaskEditStates.edit_task_description)


@router.message(F.text, TaskEditStates.edit_task_description)
async def edit_description(
        message: Message,
        state: FSMContext,
        db_conn: sqlite3,
        lexicon: DefaultLexicon
):
    new_task_description = message.text
    # Task description is too long
    if len(new_task_description) > constants.MAX_TASK_DESCRIPTION_LENGTH:
        await message.answer(
            lexicon.msg_too_long_task_name.format(
                max_task_name_length=constants.MAX_TASK_DESCRIPTION_LENGTH
            )
        )

    task: Task = (await state.get_data())['task']
    # Edit the task of the task with the provided task_id
    db.edit_task_description(db_conn, new_task_description, task.task_id, task.user_id)
    await message.answer(
        lexicon.msg_task_description_edited,
        reply_markup=keyboards.get_task_edit_kb(lexicon)
    )
    # Return to the edit keyboard state
    await state.set_state(TaskEditStates.menu)


@router.message(F.text, TaskEditStates.menu)
async def delete_task(
        message: Message,
        state: FSMContext,
        lexicon: DefaultLexicon,
):
    # User wants to delete the task
    # First, show the confirmation button
    task: Task = (await state.get_data())['task']
    await message.answer(
        lexicon.msg_delete_task_confirm.format(task_name=task.name),
        reply_markup=keyboards.get_task_deletion_confirm(lexicon)
    )
    # Then change the state
    await state.set_state(TaskEditStates.delete_task_confirm_menu)


@router.message(
    lambda message, lexicon: message.text == lexicon.kb_delete_task_confirm,
    TaskEditStates.delete_task_confirm_menu
)
async def delete_task_confirm(
        message: Message,
        state: FSMContext,
        db_conn: sqlite3,
        lexicon: DefaultLexicon
):
    task: Task = (await state.get_data())['task']
    # Delete the task with task_id
    db.delete_task(db_conn, task.task_id, task.user_id)
    await message.answer(
        lexicon.msg_task_deleted,
        reply_markup=keyboards.get_task_edit_kb(lexicon)
    )
    # Return to the edit keyboard state
    await state.set_state(TaskEditStates.menu)


@router.message(
    lambda message, lexicon: message.text == lexicon.kb_delete_task_cancel,
    TaskEditStates.delete_task_confirm_menu
)
async def delete_task_cancel(
        message: Message,
        state: FSMContext,
        lexicon: DefaultLexicon
):
    # User cancels the deletion of the task
    await message.answer(
        text=lexicon.msg_delete_task_cancel,
        reply_markup=keyboards.get_task_edit_kb(lexicon)
    )
    await state.set_state(TaskEditStates.menu)

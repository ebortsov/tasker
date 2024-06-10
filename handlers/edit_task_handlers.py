"""
This module contains handlers related to editing of the tasks. To edit the task, user must enter the command in the following format:
/edit_task_{task_id}
where task_id is a rowid attribute of a task record in the database
See form_completed_tasks() in module simple_lexicon.py to know how user enters these commands
"""
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.states import TaskCreationStates
from states.states import TaskEditStates

from lexicon.simple_lexicion import DefaultLexicon
from keyboards import keyboards
from task.task import Task
from db import db
from db.exceptions import NoUpdateError

router = Router()


@router.message(
    lambda message: message.text.startswith('/edit_task'),
    TaskCreationStates.main_menu,
)
async def show_task_edit_menu(message: Message, state: FSMContext, lexicon: DefaultLexicon):
    await message.answer(
        text=lexicon.msg_show_edit_task_menu,
        reply_markup=keyboards.get_task_edit_kb(lexicon)
    )
    await state.set_state(TaskEditStates.menu)


@router.message(
    lambda message, lexicon: message.text == lexicon.kb_cancel_task_edit,
    TaskEditStates.menu
)
async def cancel_task_edit(message: Message, state: FSMContext, lexicon: DefaultLexicon):
    await message.answer(
        text=lexicon.msg_cancel_task_edit,
        reply_markup=keyboards.get_start_kb(lexicon)
    )
    await state.set_state(TaskCreationStates.main_menu)


# @router.message(
#     lambda message: message.text.startswith('/edit_name'),
#     TaskStates.main_menu
# )
# async def edit_name_enter(
#         message: Message,
#         state: FSMContext,
#         lexicon: DefaultLexicon
# ):
#     # User wants to edit name of the task
#     user_id = message.from_user.id
#
#     await message.answer(
#         text=lexicon.msg_edit_task_name,
#         reply_markup=ReplyKeyboardRemove()
#     )
#
#     # Parse task_id from the command and save it in the state data
#     await state.set_data({'task_id': int(message.text.split('_')[-1])})
#     # Change state
#     await state.set_state(TaskStates.edit_task_name)
#
#
# @router.message(F.text, TaskStates.edit_task_name)
# async def edit_name(
#         message: Message,
#         state: FSMContext,
#         db_conn: sqlite3,
#         lexicon: DefaultLexicon
# ):
#     new_task_name = message.text
#     task_id: int = (await state.get_data())['task_id']
#
#     try:
#         # Try to edit the task of the task with the provided task_id
#         db.edit_task_name(db_conn, new_task_name, task_id, message.from_user.id)
#         await message.answer(
#             lexicon.msg_task_name_edited,
#             reply_markup=keyboards.get_start_kb(lexicon)
#         )
#     except NoUpdateError:
#         # This exception means that nothing was updated in the database
#         await message.answer(
#             lexicon.msg_task_edit_error,
#             reply_markup=keyboards.get_start_kb(lexicon)
#         )
#     finally:
#         # In any case, just return to the main menu
#         await state.set_state(TaskStates.main_menu)
#         # ... And delete all data
#         await state.set_data({})

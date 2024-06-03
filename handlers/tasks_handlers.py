from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import html
from aiogram import F
from aiogram.fsm.context import FSMContext
from states.states import TaskStates
from aiogram.filters import and_f, or_f

from lexicon.simple_lexicion import DefaultLexicon
from keyboards import keyboards

router = Router()


@router.message(
    lambda message, lexicon: message.text == lexicon.kb_start_new_task,
    TaskStates.main_menu
)
async def start_new_task(message: Message, state: FSMContext, lexicon: DefaultLexicon):
    # User wants to start the new task
    # Prompt the user to enter the name of the new task
    await message.answer(
        text=lexicon.msg_new_task_name_enter_prompt,
        reply_markup=keyboards.get_cancel_kb(lexicon)
    )
    # Switch the state
    await state.set_state(TaskStates.new_task_name_enter)


@router.message(
    F.text == 'Cancel',
    TaskStates.new_task_name_enter
)
async def new_task_name_enter_cancel(message: Message, state: FSMContext, lexicon: DefaultLexicon):
    # User wants to cancel the start of the new task
    await message.answer(
        text=lexicon.msg_new_task_cancelled,
        reply_markup=keyboards.get_start_kb(lexicon)
    )
    # Switch the state
    await state.set_state(TaskStates.main_menu)


@router.message(TaskStates.new_task_name_enter)
async def new_task_name_enter(message: Message, state: FSMContext, lexicon: DefaultLexicon):
    # User entered the name of the task. Now we need to start the new task

    # Remember the name and the start time of the task
    await state.update_data(taskname=message.text)

    await message.answer(
        text=lexicon.msg_ongoing_task_start.format(taskname=html.quote(message.text)),
        reply_markup=keyboards.get_ongoing_task_kb(lexicon)
    )

    # Switch the state
    await state.set_state(TaskStates.ongoing_task)


@router.message(
    lambda message, lexicon: message.text == lexicon.kb_cancel_ongoing_task,
    TaskStates.ongoing_task
)
async def cancel_ongoing_task_confirm(message: Message, state: FSMContext, lexicon: DefaultLexicon):
    # User wants to cancel the ongoing task
    # In this handler we want to receive confirmation in task cancellation
    await message.answer(
        text=lexicon.msg_cancel_ongoing_task_confirm,
        reply_markup=keyboards.get_cancel_ongoing_task_confirm_kb(lexicon)
    )
    await state.set_state(TaskStates.ongoing_task_cancel_confirm)


@router.message(
    lambda message, lexicon: message.text == lexicon.kb_cancel_ongoing_task_confirm,
    TaskStates.ongoing_task_cancel_confirm
)
async def kill_task(message: Message, state: FSMContext, lexicon: DefaultLexicon):
    # User confirms that they want to cancel the task
    taskname = (await state.get_data())['taskname']
    await message.answer(
        text=lexicon.msg_task_killed.format(taskname=taskname),
        reply_markup=keyboards.get_start_kb(lexicon)
    )

    # Clear the state data and return to the main menu
    await state.set_data({})
    await state.set_state(TaskStates.main_menu)


@router.message(
    and_f(
        lambda message, lexicon: message.text == lexicon.kb_continue_ongoing_task,
        or_f(TaskStates.ongoing_task_cancel_confirm, TaskStates.finish_ongoing_task_confirm)
    )
)
async def continue_task(message: Message, state: FSMContext, lexicon: DefaultLexicon):
    # User wants to continue the task (applies to both cancellation and finalization of the task)
    taskname = (await state.get_data())['taskname']
    await message.answer(
        text=lexicon.msg_continue_task.format(taskname=taskname),
        reply_markup=keyboards.get_ongoing_task_kb(lexicon)
    )
    await state.set_state(TaskStates.ongoing_task)


@router.message(
    lambda message, lexicon: message.text == lexicon.kb_finish_ongoing_task,
    TaskStates.ongoing_task
)
async def finish_task_confirm(message: Message, state: FSMContext, lexicon: DefaultLexicon):
    # User wants to finish current task
    taskname = (await state.get_data())['taskname']
    await message.answer(
        text=lexicon.msg_finish_ongoing_task_confirm.format(taskname=taskname),
        reply_markup=keyboards.get_finish_task_confirm_kb(lexicon)
    )
    await state.set_state(TaskStates.finish_ongoing_task_confirm)

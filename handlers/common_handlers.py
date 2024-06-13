from aiogram import Router
from aiogram import types
from aiogram.filters import Command
from aiogram import html
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from states.states import TaskCreationStates

from lexicon.simple_lexicion import DefaultLexicon
from keyboards import keyboards

router = Router()


@router.message(Command('start'))
async def start_command(message: types.Message, state: FSMContext, lexicon: DefaultLexicon):
    await message.answer(
        text=lexicon.msg_start_command,
        reply_markup=keyboards.get_start_kb(lexicon)
    )
    await state.set_state(TaskCreationStates.main_menu)
    await state.set_data({})

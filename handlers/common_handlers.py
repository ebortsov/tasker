from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards import keyboards
from lexicon.simple_lexicion import DefaultLexicon
from states.states import TaskCreationStates

router = Router()


@router.message(Command('start'))
async def start_command(message: types.Message, state: FSMContext, lexicon: DefaultLexicon):
    await message.answer(
        text=lexicon.msg_start_command, reply_markup=keyboards.get_start_kb(lexicon)
    )
    await state.set_state(TaskCreationStates.main_menu)
    await state.set_data({})

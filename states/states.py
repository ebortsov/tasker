from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup


class TaskStates(StatesGroup):
    main_menu = State()
    new_task_name_enter = State()
    ongoing_task = State()
    ongoing_task_cancel_confirm = State()
    finish_ongoing_task_confirm = State()
    completed_task_desc_enter = State()

from dataclasses import dataclass
from aiogram import html


@dataclass
class DefaultLexicon:
    msg_start_command: str = (
        f"{html.bold('Welcome')} to my task manager bot!\n"
        f"This bot provides a convenient way to {html.bold('create')}💫 and {html.bold('track')}📝 "
        f"your study, work, or any other type of tasks📋"
    )
    msg_new_task_name_enter_prompt: str = 'Please, enter the title of the task:'
    msg_new_task_cancelled: str = 'The creation of the new task has been cancelled'
    msg_ongoing_task_start: str = 'The new task «{taskname}» has been started!⭐️'
    msg_cancel_ongoing_task_confirm: str = 'Are you sure you want to cancel current task?'
    msg_task_killed: str = 'The task «{taskname}» has been cancelled🛑'
    msg_continue_task: str = 'Alright, so you are keep doing «{taskname}»'
    msg_finish_ongoing_task_confirm: str = 'Are you sure you want to finish the task: «{taskname}»?'

    kb_show_prev_tasks: str = 'Show previous tasks'
    kb_start_new_task: str = 'Start new task'
    kb_cancel_task_creation: str = 'Cancel'
    kb_cancel_ongoing_task: str = 'Cancel ongoing task'
    kb_finish_ongoing_task: str = 'Finish ongoing task'
    kb_cancel_ongoing_task_confirm: str = 'Confirm cancellation'
    kb_continue_ongoing_task: str = 'Continue task'
    kb_finish_ongoing_task_confirm: str = 'Finish task!'


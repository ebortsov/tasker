from dataclasses import dataclass
from aiogram import html
from task.task import Task
from aiogram import html


@dataclass
class DefaultLexicon:
    msg_start_command: str = (
        f"{html.bold('Welcome')} to my task manager bot!\n"
        f"This bot provides a convenient way to {html.bold('create')}💫 and {html.bold('track')}📝 "
        f"your study, work, or any other type of tasks📋"
    )
    msg_new_task_name_enter_prompt: str = 'Please, enter the title of the task:'
    msg_too_long_task_name: str = (
        'The length of the task name must '
        'not exceed {max_task_name_length} characters'
    )
    msg_new_task_cancelled: str = 'The creation of the new task has been cancelled'
    msg_ongoing_task_start: str = 'The new task «{task_name}» has been started!⭐️'
    msg_cancel_ongoing_task_confirm: str = 'Are you sure you want to cancel current task?'
    msg_task_killed: str = 'The task «{task_name}» has been cancelled🛑'
    msg_continue_task: str = 'Alright, so you are keep doing «{task_name}»'
    msg_finish_ongoing_task_confirm: str = 'Are you sure you want to finish the task: «{task_name}»?'
    msg_enter_task_description: str = 'Cool! Enter what you have done:'
    msg_task_completed: str = (
        'The task «{task_name}» has been '
        f'{html.bold("completed")}!\n'
        'You have been working on it for {hours} hours {minutes} minutes'
    )
    msg_no_completed_tasks: str = 'You haven\'t completed any tasks yet!'
    msg_too_long_description: str = (
        'The length of the description must '
        'not exceed {max_task_description_length} characters'
    )
    msg_edit_task_name = 'Please, enter the new name of the task:'
    msg_task_name_edited = 'The task name has been changed✅'
    msg_edit_task_description = 'Please, enter the new description of the task:'
    msg_task_description_edited = 'The task description has been changed✅'
    msg_delete_task_confirm = 'Are you sure you want to delete task «{task_name}»?'
    msg_task_deleted = 'The task has been deleted✅'
    msg_delete_task_cancel = 'Task deletion has been cancelled'
    msg_show_edit_task_menu = 'There you can choose how you want to edit your task'
    msg_cancel_task_edit = 'The task edit has been cancelled'
    msg_no_such_task = 'There is no such task!🙈'

    kb_show_prev_tasks: str = 'Show previous tasks'
    kb_start_new_task: str = 'Start new task'
    kb_cancel_task_creation: str = 'Cancel task creation'
    kb_cancel_ongoing_task: str = 'Cancel ongoing task'
    kb_finish_ongoing_task: str = 'Finish ongoing task'
    kb_cancel_ongoing_task_confirm: str = 'Confirm cancellation'
    kb_continue_ongoing_task: str = 'Continue task'
    kb_finish_ongoing_task_confirm: str = 'Finish task!'
    kb_back_to_main_menu_from_edit_menu: str = 'Back to main menu'
    kb_edit_task_name: str = 'Edit task name'
    kb_edit_task_description: str = 'Edit task description'
    kb_delete_task: str = 'Delete task'
    kb_delete_task_confirm: str = 'Yes, I want to delete this task'
    kb_delete_task_cancel: str = 'Cancel deletion'
    kb_next_page: str = '▶️'
    kb_prev_page: str = '️️◀️'

    @staticmethod
    def form_task(task: Task) -> str:
        result = (
                html.bold('Title: ') + html.quote(task.name) + '\n' +
                html.bold('Description: ') + html.quote(task.desc) + '\n' +
                f'✏️ /edit_task_{task.task_id}\n\n'
        )
        return result

from dataclasses import dataclass

from aiogram import html

from task.task import Task


@dataclass
class DefaultLexicon:
    msg_start_command: str = (
        f"{html.bold('Welcome')} to my task manager bot!\n"
        f"This bot provides a convenient way to {html.bold('create')}💫 and {html.bold('track')}📝 "
        f"your study, work, or any other type of tasks📋\n\n"
        f"Use the menu to change your UTC offset ({html.bold('initially, the offset is set to 00:00')})"
    )
    msg_new_task_name_enter_prompt: str = 'Please, enter the title of the task:'
    msg_too_long_task_name: str = (
        'The length of the task name must ' 'not exceed {max_task_name_length} characters'
    )
    msg_new_task_cancelled: str = 'The creation of the new task has been cancelled'
    msg_ongoing_task_start: str = 'The new task «{task_name}» has been started!⭐️'
    msg_cancel_ongoing_task_confirm: str = 'Are you sure you want to cancel current task?'
    msg_task_killed: str = 'The task «{task_name}» has been cancelled🛑'
    msg_continue_task: str = 'Alright, so you are keep doing «{task_name}»'
    msg_finish_ongoing_task_confirm: str = (
        'Are you sure you want to finish the task: «{task_name}»?'
    )
    msg_enter_task_description: str = 'Cool! Enter what you have done:'
    msg_task_completed: str = (
        "The task «{task_name}» has been "
        f'{html.bold("completed")}!\n'
        "You have been working on it for {hours} hours {minutes} minutes"
    )
    msg_no_completed_tasks: str = "You haven't completed any tasks yet!"
    msg_too_long_description: str = (
        'The length of the description must ' 'not exceed {max_task_description_length} characters'
    )
    msg_edit_task_name = 'Please, enter the new name of the task:'
    msg_task_name_edited = 'The task name has been changed✅'
    msg_edit_task_description = 'Please, enter the new description of the task:'
    msg_task_description_edited = 'The task description has been changed✅'
    msg_delete_task_confirm = 'Are you sure you want to delete task «{task_name}»?'
    msg_task_deleted = 'The task has been deleted✅'
    msg_delete_task_cancel = 'Task deletion has been cancelled'
    msg_show_edit_task_menu = 'There you can choose how you want to edit your task'
    msg_cancel_task_edit = 'Returned to main menu'
    msg_no_such_task = 'There is no such task!🙈'
    msg_use_start = 'Please, use the command /start to start the bot'
    msg_restart_the_bot_because_of_error = (
        'Oops, looks like some pretty bad error occurred!\n'
        'To use the bot please, call the command /start again'
    )
    msg_select_utc_offset = 'Select your offset from UTC'
    msg_utc_offset_updated = 'You UTC offset🕔 has been successfully updated!'

    kb_show_prev_tasks: str = 'Show previous tasks'
    kb_start_new_task: str = 'Start new task'
    kb_update_utc_offset: str = 'Set your UTC offset'
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
        time_string = ''
        if task.start_time and task.end_time and task.start_time.day == task.end_time.day:
            time_string = (
                f"{html.bold('Duration: ')}{html.italic(task.start_time.strftime('%d-%m-%Y'))} "
                f"({task.start_time.strftime('%H:%M:%S')} — "
                f"{task.end_time.strftime('%H:%M:%S')})\n"
            )
        elif task.start_time and task.end_time:
            time_string = (
                f"{html.bold('Duration: ')}"
                f"{html.italic(task.start_time.strftime('%d-%m-%Y'))} "
                f"{task.start_time.strftime('%H:%M:%S')} — "
                f"{html.italic(task.end_time.strftime('%d-%m-%Y'))} "
                f"{task.end_time.strftime('%H:%M:%S')}\n"
            )

        result = (
            time_string
            + html.bold('Title: ')
            + html.quote(task.name)
            + '\n'
            + html.bold('Description: ')
            + html.quote(task.desc)
            + '\n'
            + f'✏️ /edit_task_{task.task_id}\n\n'
        )
        return result

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

    kb_show_prev_tasks: str = 'Show previous tasks'
    kb_start_new_task: str = 'Start new task'
    kb_cancel_task_creation: str = 'Cancel'
    kb_cancel_ongoing_task: str = 'Cancel ongoing task'
    kb_finish_ongoing_task: str = 'Finish ongoing task'
    kb_cancel_ongoing_task_confirm: str = 'Confirm cancellation'
    kb_continue_ongoing_task: str = 'Continue task'
    kb_finish_ongoing_task_confirm: str = 'Finish task!'

    @staticmethod
    def form_completed_tasks(completed_tasks: list[Task]) -> str:
        result = '\n\n'.join(
            html.bold('Title: ') + html.quote(task.name) + '\n' +
            html.bold('Description: ') + html.quote(task.desc)
            for task in completed_tasks
        )
        return result

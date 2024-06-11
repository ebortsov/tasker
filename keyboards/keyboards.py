from aiogram.types import (
    KeyboardButton,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from lexicon.simple_lexicion import DefaultLexicon


def form_kb(*button_texts: str, width: int = 1) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(*[KeyboardButton(text=button_text) for button_text in button_texts], width=width)
    return builder.as_markup(resize_keyboard=True)


def get_start_kb(lexicon: DefaultLexicon = DefaultLexicon) -> ReplyKeyboardMarkup:
    return form_kb(lexicon.kb_start_new_task, lexicon.kb_show_prev_tasks, width=2)


def get_cancel_kb(lexicon: DefaultLexicon = DefaultLexicon) -> ReplyKeyboardMarkup:
    return form_kb(lexicon.kb_cancel_task_creation)


def get_ongoing_task_kb(lexicon: DefaultLexicon = DefaultLexicon) -> ReplyKeyboardMarkup:
    return form_kb(lexicon.kb_cancel_ongoing_task, lexicon.kb_finish_ongoing_task)


def get_cancel_ongoing_task_confirm_kb(lexicon: DefaultLexicon = DefaultLexicon) -> ReplyKeyboardMarkup:
    return form_kb(lexicon.kb_cancel_ongoing_task_confirm, lexicon.kb_continue_ongoing_task, width=2)


def get_finish_task_confirm_kb(lexicon: DefaultLexicon = DefaultLexicon) -> ReplyKeyboardMarkup:
    return form_kb(lexicon.kb_finish_ongoing_task_confirm, lexicon.kb_continue_ongoing_task, width=2)


def get_task_edit_kb(lexicon: DefaultLexicon = DefaultLexicon) -> ReplyKeyboardMarkup:
    return form_kb(
        lexicon.kb_back_to_main_menu_from_edit_menu,
        lexicon.kb_edit_task_name,
        lexicon.kb_edit_task_description,
        lexicon.kb_delete_task,
        width=2
    )


def get_task_deletion_confirm(lexicon: DefaultLexicon = DefaultLexicon) -> ReplyKeyboardMarkup:
    return form_kb(
        lexicon.kb_delete_task_cancel,
        lexicon.kb_delete_task_confirm,
        width=2
    )

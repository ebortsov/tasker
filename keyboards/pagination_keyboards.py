from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from page.page import Page
from lexicon.simple_lexicion import DefaultLexicon
from handlers.pagination.callback_data import SwitchPageCallback


def get_next_button(page_num: int, lexicon: DefaultLexicon) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=lexicon.kb_next_page,
        callback_data=SwitchPageCallback(page_num=page_num).pack()
    )


def get_prev_button(page_num: int, lexicon: DefaultLexicon) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=lexicon.kb_prev_page,
        callback_data=SwitchPageCallback(page_num=page_num).pack()
    )


def get_corresponding_keyboard(page: Page, lexicon: DefaultLexicon) -> InlineKeyboardMarkup | None:
    if page.page_num == 1 and page.is_last_page:
        # No reason to show the keyboard if there is only one page in total
        return None

    builder = InlineKeyboardBuilder()
    # Page is not the first page
    if page.page_num > 1:
        builder.add(get_prev_button(page.page_num - 1, lexicon))
    # Page isn't the last page
    if not page.is_last_page:
        builder.add(get_next_button(page.page_num + 1, lexicon))

    return builder.as_markup()

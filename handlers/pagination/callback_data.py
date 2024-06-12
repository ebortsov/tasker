from aiogram.filters.callback_data import CallbackData


class SwitchPageCallback(CallbackData, prefix='switch_page'):
    page_num: int

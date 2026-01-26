from aiogram.types import (
     InlineKeyboardMarkup, InlineKeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder


def start_inline_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()
    markup.add(
        InlineKeyboardButton(text='🔍 Проверить уровень английского', callback_data='check'),
        InlineKeyboardButton(text='📘 Информация о курсе', callback_data='info')
    )
    return markup.as_markup()

def application_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()
    markup.add(
        InlineKeyboardButton(text="📝 Оставить заявку на курс", callback_data='application'),
        InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")
    )
    return markup.adjust(1).as_markup()
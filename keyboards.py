# keyboards.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu():
    buttons = [
        [InlineKeyboardButton(text="🌟 Характер (плюсы/минусы)", callback_data="detail_character")],
        [InlineKeyboardButton(text="🔮 Кармические задачи", callback_data="detail_karma")],
        [InlineKeyboardButton(text="💰 Денежный канал", callback_data="detail_money")],
        [InlineKeyboardButton(text="❤️ Линия любви", callback_data="detail_love")],
        [InlineKeyboardButton(text="🛋 Зона комфорта", callback_data="detail_comfort")],
        [InlineKeyboardButton(text="🌳 Детско-родительская карма", callback_data="detail_family_parents")],
        [InlineKeyboardButton(text="🌀 Родовые задачи и исцеление", callback_data="detail_family_rod")],
        [InlineKeyboardButton(text="📩 Записаться на консультацию", callback_data="consultation")],
        [InlineKeyboardButton(text="🔄 Рассчитать заново", callback_data="restart")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_back_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад к сводке", callback_data="back_to_summary")]
        ]
    )
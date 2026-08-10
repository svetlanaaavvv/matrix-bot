# bot.py
import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from calculator import calculate_matrix
from meanings import get_archan
from keyboards import get_main_menu, get_back_button
from subscribe import check_subscription, get_subscribe_keyboard

# Настройка логирования
logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    logging.error("❌ BOT_TOKEN не найден!")
    exit(1)

storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=storage)

class Form(StatesGroup):
    waiting_for_date = State()
    waiting_for_subscribe = State()

user_data = {}

# ------------------ ОСНОВНЫЕ ФУНКЦИИ ------------------

def format_summary(matrix):
    result = "🔮 ВАША МАТРИЦА СУДЬБЫ\n\n"
    result += "Расчёт выполнен по дате рождения\n"
    result += "------------------------------\n\n"
    
    positions = {
        "character": "🌟 Характер",
        "karma": "🔮 Кармические задачи",
        "money": "💰 Денежный канал",
        "love": "❤️ Линия любви",
        "comfort": "🛋 Зона комфорта"
    }
    
    for key, title in positions.items():
        archan_num = matrix.get(key)
        archan = get_archan(archan_num)
        if archan:
            name = archan.get("name", "")
            plus = archan.get("character", {}).get("plus", "")
            short = plus[:120] + "..." if len(plus) > 120 else plus
            result += f"{title} — {archan_num} Аркан {name}\n"
            result += f"   {short}\n\n"
    
    result += "------------------------------\n\n"
    result += "👇 Нажмите на кнопку, чтобы узнать подробную трактовку:\n\n"
    result += "💬 Для полного разбора и личной консультации напишите мне в Telegram:\n"
    result += "👉 @svetlanaaa_vv"
    return result

def format_detail(archan_num, detail_type):
    archan = get_archan(archan_num)
    if not archan:
        return "❌ Аркан не найден"
    
    name = archan.get("name", "")
    
    detail_map = {
        "character": {
            "title": f"🌟 Характер — {archan_num} Аркан {name}",
            "text": f"✅ В плюсе:\n{archan.get('character', {}).get('plus', 'Нет данных')}\n\n❌ В минусе:\n{archan.get('character', {}).get('minus', 'Нет данных')}"
        },
        "karma": {
            "title": f"🔮 Кармические задачи — {archan_num} Аркан {name}",
            "text": f"✅ В плюсе:\n{archan.get('karma', {}).get('plus', 'Нет данных')}\n\n❌ В минусе:\n{archan.get('karma', {}).get('minus', 'Нет данных')}"
        },
        "money": {
            "title": f"💰 Денежный канал — {archan_num} Аркан {name}",
            "text": f"✅ В плюсе:\n{archan.get('money', {}).get('plus', 'Нет данных')}\n\n❌ В минусе:\n{archan.get('money', {}).get('minus', 'Нет данных')}"
        },
        "love": {
            "title": f"❤️ Линия любви — {archan_num} Аркан {name}",
            "text": f"✅ В плюсе:\n{archan.get('love', {}).get('plus', 'Нет данных')}\n\n❌ В минусе:\n{archan.get('love', {}).get('minus', 'Нет данных')}"
        },
        "comfort": {
            "title": f"🛋 Зона комфорта — {archan_num} Аркан {name}",
            "text": f"✅ В плюсе:\n{archan.get('comfort', {}).get('plus', 'Нет данных')}\n\n❌ В минусе:\n{archan.get('comfort', {}).get('minus', 'Нет данных')}"
        },
        "family_parents": {
            "title": f"🌳 Детско-родительская карма — {archan_num} Аркан {name}",
            "text": f"🚫 Ошибки:\n{archan.get('family_parents', {}).get('errors', 'Нет данных')}\n\n🎯 К чему прийти:\n{archan.get('family_parents', {}).get('goal', 'Нет данных')}\n\n👶 Чему учит ребёнок:\n{archan.get('family_parents', {}).get('child_lesson', 'Нет данных')}"
        },
        "family_rod": {
            "title": f"🌀 Родовые задачи — {archan_num} Аркан {name}",
            "text": f"🚫 Блоки в роду:\n{archan.get('family_rod', {}).get('blocks', 'Нет данных')}\n\n🎯 Задачи:\n{archan.get('family_rod', {}).get('tasks', 'Нет данных')}\n\n✨ Бонусы при исцелении:\n{archan.get('family_rod', {}).get('bonus', 'Нет данных')}"
        }
    }
    
    detail = detail_map.get(detail_type)
    if not detail:
        return "❌ Раздел не найден"
    
    result = f"{detail['title']}\n\n{detail['text']}\n\n"
    result += "------------------------------\n\n"
    result += "💬 Для полного разбора и личной консультации напишите мне в Telegram:\n"
    result += "👉 @svetlanaaa_vv"
    
    return result

# ------------------ ОБРАБОТЧИК КОМАНДЫ /start ------------------

@dp.message(Command("start"))
async def start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    
    is_subscribed = await check_subscription(message.bot, user_id)
    
    if not is_subscribed:
        await message.answer(
            "🔒 ДОБРО ПОЖАЛОВАТЬ!\n\n"
            "Но сначала подпишитесь на мой канал, чтобы получить доступ к боту:\n\n"
            "👇 Нажмите на кнопку, подпишитесь, а затем нажмите «✅ Я ПОДПИСАЛСЯ»\n\n"
            "Это бесплатно и займёт 5 секунд!\n"
            "После подписки бот откроет все возможности 🔮",
            reply_markup=get_subscribe_keyboard()
        )
        await state.set_state(Form.waiting_for_subscribe)
        return
    
    welcome_text = (
        "🔮 ДОБРО ПОЖАЛОВАТЬ В МАТРИЦУ СУДЬБЫ!\n\n"
        "Я помогу вам узнать ваши ключевые арканы:\n\n"
        "🌟 Характер — ваши сильные и слабые стороны\n"
        "🔮 Кармические задачи — уроки души\n"
        "💰 Денежный канал — как приходят деньги\n"
        "❤️ Линия любви — сценарии в отношениях\n"
        "🛋 Зона комфорта — что приносит удовлетворение\n\n"
        "📅 Введите дату рождения в формате ДД.ММ.ГГГГ\n"
        "Например: 15.07.1990\n\n"
        "💬 Для полного разбора и личной консультации напишите мне в Telegram: @svetlanaaa_vv"
    )
    await message.answer(welcome_text)
    await state.set_state(Form.waiting_for_date)

# ------------------ ОБРАБОТЧИК ПРОВЕРКИ ПОДПИСКИ ------------------

@dp.callback_query(lambda c: c.data == "check_subscribe")
async def check_subscribe_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    
    is_subscribed = await check_subscription(callback.bot, user_id)
    
    if is_subscribed:
        await callback.message.edit_text(
            "✅ СПАСИБО ЗА ПОДПИСКУ!\n\n"
            "🔮 Теперь я могу показать вашу Матрицу Судьбы.\n\n"
            "📅 Введите дату рождения в формате ДД.ММ.ГГГГ\n"
            "Например: 15.07.1990\n\n"
            "💬 Для полного разбора и личной консультации напишите мне в Telegram: @svetlanaaa_vv"
        )
        await state.set_state(Form.waiting_for_date)
        await callback.answer()
    else:
        await callback.answer(
            "❌ Вы ещё не подписались на канал!\n"
            "Нажмите кнопку и подпишитесь, затем нажмите «Я ПОДПИСАЛСЯ»",
            show_alert=True
        )

# ------------------ ОБРАБОТЧИК КОМАНДЫ /subscribe ------------------

@dp.message(Command("subscribe"))
async def subscribe_command(message: Message):
    user_id = message.from_user.id
    
    is_subscribed = await check_subscription(message.bot, user_id)
    
    if is_subscribed:
        await message.answer(
            "✅ ВЫ УЖЕ ПОДПИСАНЫ НА КАНАЛ!\n\n"
            "🔮 Введите дату рождения, чтобы начать.\n\n"
            "💬 Для полного разбора и личной консультации напишите мне в Telegram: @svetlanaaa_vv"
        )
    else:
        await message.answer(
            "🔒 ПОДПИШИТЕСЬ НА КАНАЛ ДЛЯ ДОСТУПА!\n\n"
            "Нажмите на кнопку ниже, подпишитесь, "
            "а затем нажмите «✅ Я ПОДПИСАЛСЯ»",
            reply_markup=get_subscribe_keyboard()
        )

# ------------------ ОБРАБОТЧИК КНОПКИ КОНСУЛЬТАЦИИ ------------------

@dp.callback_query(lambda c: c.data == "consultation")
async def consultation_callback(callback: CallbackQuery):
    await callback.message.answer(
        "📩 ЗАПИСЬ НА КОНСУЛЬТАЦИЮ\n\n"
        "Для полного разбора вашей Матрицы Судьбы и личной консультации:\n\n"
        "👇 Напишите мне в Telegram:\n"
        "👉 @svetlanaaa_vv\n\n"
        "Я помогу вам глубже понять ваши арканы и дам персональные рекомендации."
    )
    await callback.answer()

# ------------------ ОБРАБОТЧИК ВВОДА ДАТЫ ------------------

@dp.message(Form.waiting_for_date)
async def get_date(message: Message, state: FSMContext):
    date_str = message.text.strip()
    
    try:
        day, month, year = map(int, date_str.split('.'))
        if day < 1 or day > 31 or month < 1 or month > 12 or year < 1900 or year > 2100:
            raise ValueError
    except:
        await message.answer("❌ Неверный формат. Введите дату как ДД.ММ.ГГГГ (например, 15.07.1990)")
        return
    
    matrix = calculate_matrix(date_str)
    if not matrix:
        await message.answer("❌ Ошибка расчёта. Попробуйте ещё раз.")
        return
    
    user_id = message.from_user.id
    user_data[user_id] = matrix
    
    summary = format_summary(matrix)
    await message.answer(summary, reply_markup=get_main_menu())
    await state.clear()

# ------------------ ОБРАБОТЧИК КНОПОК ------------------

@dp.callback_query()
async def handle_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    matrix = user_data.get(user_id)
    
    if not matrix:
        await callback.message.edit_text("❌ Данные не найдены. Начните заново: /start")
        await callback.answer()
        return
    
    if callback.data == "restart":
        await callback.message.edit_text("🔄 Введите новую дату рождения в формате ДД.ММ.ГГГГ")
        await state.set_state(Form.waiting_for_date)
        await callback.answer()
        return
    
    if callback.data == "back_to_summary":
        summary = format_summary(matrix)
        await callback.message.edit_text(summary, reply_markup=get_main_menu())
        await callback.answer()
        return
    
    if callback.data.startswith("detail_"):
        detail_type = callback.data.replace("detail_", "")
        
        archan_num = None
        if detail_type in ["character", "karma", "money", "love", "comfort"]:
            archan_num = matrix.get(detail_type)
        elif detail_type in ["family_parents", "family_rod"]:
            archan_num = matrix.get("comfort")
        
        if not archan_num:
            await callback.message.edit_text("❌ Данные не найдены")
            await callback.answer()
            return
        
        detail_text = format_detail(archan_num, detail_type)
        await callback.message.edit_text(
            detail_text,
            reply_markup=get_back_button()
        )
        await callback.answer()

@dp.message()
async def unknown(message: Message):
    await message.answer(
        "❌ Я не понимаю эту команду.\n"
        "Чтобы начать, нажмите /start или введите дату рождения.\n\n"
        "💬 Для полного разбора и личной консультации напишите мне в Telegram: @svetlanaaa_vv"
    )

async def main():
    logging.info("🚀 Бот Матрицы Судьбы запускается...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
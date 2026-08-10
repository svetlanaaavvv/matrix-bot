# subscribe.py
import logging
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

logger = logging.getLogger(__name__)

# Данные вашего канала
CHANNEL_ID = "@svetlanaaa_vv1"  # ID вашего канала
CHANNEL_LINK = "https://t.me/svetlanaaa_vv1"  # Ссылка на канал


def get_subscribe_keyboard():
    """Клавиатура для кнопки подписки"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 ПОДПИСАТЬСЯ НА КАНАЛ",
                    url=CHANNEL_LINK
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ Я ПОДПИСАЛСЯ",
                    callback_data="check_subscribe"
                )
            ]
        ]
    )


async def check_subscription(bot: Bot, user_id: int) -> bool:
    """
    Проверяет, подписан ли пользователь на канал
    Возвращает True, если подписан
    """
    try:
        member = await bot.get_chat_member(
            chat_id=CHANNEL_ID,
            user_id=user_id
        )
        
        if member.status in ["member", "administrator", "creator"]:
            logger.info(f"✅ Пользователь {user_id} подписан на канал")
            return True
        else:
            logger.info(f"❌ Пользователь {user_id} НЕ подписан на канал")
            return False
            
    except Exception as e:
        logger.warning(f"⚠️ Ошибка проверки подписки: {e}")
        # При ошибке пропускаем проверку (чтобы бот работал)
        return True
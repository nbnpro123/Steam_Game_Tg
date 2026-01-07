# main.py - Полный код бота в одном файле

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from steam_parser import get_top_games, get_discount_games, get_free_games
import time
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SteamGameBot:
    """Класс для управления ботом Steam"""

    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.setup_handlers()

    def setup_handlers(self):
        """Настройка обработчиков команд"""

        @self.bot.message_handler(commands=['start'])
        def cmd_start(message):
            welcome_text = (
                "🎮 *Добро пожаловать в Steam Game Bot!*\n\n"
                "Я могу показать вам различные категории игр из Steam.\n\n"
                "📋 *Доступные команды:*\n"
                "• /top - Топ игр по продажам\n"
                "• /discount - Игры со скидками\n"
                "• /free - Бесплатные игры\n"
                "• /help - Помощь\n\n"
                "Используйте кнопки ниже для быстрого доступа!"
            )

            keyboard = InlineKeyboardMarkup()
            keyboard.row(
                InlineKeyboardButton("🎯 Топ игр", callback_data="top_game"),
                InlineKeyboardButton("🔥 Со скидками", callback_data="top_discount")
            )
            keyboard.row(
                InlineKeyboardButton("🆓 Бесплатные", callback_data="top_free")
            )
            keyboard.row(
                InlineKeyboardButton("🔄 Обновить", callback_data="refresh"),
                InlineKeyboardButton("❓ Помощь", callback_data="help")
            )

            self.bot.send_message(
                message.chat.id,
                welcome_text,
                parse_mode='Markdown',
                reply_markup=keyboard
            )

        # Добавьте остальные хендлеры из tg_bot.py аналогичным образом

    def run(self):
        """Запуск бота"""
        print("🚀 Запуск Steam Game Bot...")
        try:
            self.bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            logger.error(f"Ошибка при работе бота: {e}")
            raise


def main():
    """Точка входа в приложение"""
    print("=" * 50)
    print("STEAM GAME BOT")
    print("=" * 50)

    # Создание и запуск бота
    token = '8304089254:AAFU7vaP8KxgXiCc5VL591P6JNaOR-gIbXc'
    bot = SteamGameBot(token)

    print("✅ Бот запущен")
    print("ℹ️  Для остановки нажмите Ctrl+C")
    print("-" * 50)

    try:
        bot.run()
    except KeyboardInterrupt:
        print("\n\n🛑 Бот остановлен пользователем")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
    finally:
        print("\n✅ Бот завершил работу")


if __name__ == "__main__":
    main()
# main.py - Главный файл для запуска Telegram бота

import telebot
from telebot import TeleBot
from steam_parser import get_top_games, get_discount_games, get_free_games
import time
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Основная функция запуска бота"""
    print("=" * 50)
    print("Запуск Steam Game Bot...")
    print("=" * 50)

    # Инициализация бота
    bot = telebot.TeleBot(token='8304089254:AAFU7vaP8KxgXiCc5VL591P6JNaOR-gIbXc')

    # Импорт хендлеров из файла бота
    import tg_bot  # или замените на актуальное имя файла с ботом

    print("✅ Бот инициализирован")
    print("ℹ️  Для остановки нажмите Ctrl+C")
    print("-" * 50)

    try:
        # Запуск бота
        bot.polling(none_stop=True, interval=0, timeout=20)

    except KeyboardInterrupt:
        print("\n\n🛑 Бот остановлен пользователем")
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {e}")
        logger.error(f"Ошибка при запуске бота: {e}")
    finally:
        print("✅ Бот завершил работу")


if __name__ == "__main__":
    main()
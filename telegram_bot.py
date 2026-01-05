from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import telebot
from steam_parser import get_top_games  # Импортируем функцию вместо переменной

bot = telebot.TeleBot(token='8304089254:AP6JNaOR-gIbXc')


@bot.message_handler(commands=['start'])
def cmd_start(message):
    """Обработчик команды /start"""
    welcome_text = (
        "🎮 *Добро пожаловать в Steam Game Bot!*\n\n"
        "Я могу показать вам топ продаж игр из Steam.\n\n"
        "📋 *Доступные команды:*\n"
        "• /top - Топ игр по продажам\n"
        "• /top10 - Топ-10 игр\n"
        "• /top20 - Топ-20 игр\n"
        "• /help - Помощь\n\n"
        "Используйте /top для начала!"
    )

    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton("🎯 Топ игр", callback_data="top_game"),
        InlineKeyboardButton("🔥 Со скидками", callback_data="top_discount")
    )
    keyboard.row(
        InlineKeyboardButton("🆓 Бесплатные", callback_data="top_free")
    )

    bot.send_message(
        message.chat.id,
        welcome_text,
        parse_mode='Markdown',
        reply_markup=keyboard
    )


@bot.message_handler(commands=['top'])
def send_top_games(message):
    """Обработчик команды /top"""
    try:
        bot.send_message(message.chat.id, "🔄 Получаю актуальный топ игр с Steam...")
        # Получаем данные через функцию
        game_top1 = get_top_games()

        # Разбиваем длинное сообщение на части, если оно слишком длинное
        if len(game_top1) > 4000:  # Ограничение Telegram
            parts = [game_top1[i:i + 4000] for i in range(0, len(game_top1), 4000)]
            for part in parts:
                bot.send_message(message.chat.id, part, disable_web_page_preview=True)
        else:
            bot.send_message(message.chat.id, game_top1, disable_web_page_preview=True)

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Произошла ошибка: {str(e)}")


@bot.callback_query_handler(func=lambda call: True)
def callback_message(callback):
    if callback.data == "top_game":
        bot.answer_callback_query(callback.id, "Загружаю топ игр...")
        try:
            # Получаем данные через функцию
            game_top1 = get_top_games()

            if len(game_top1) > 4000:
                parts = [game_top1[i:i + 4000] for i in range(0, len(game_top1), 4000)]
                for part in parts:
                    bot.send_message(callback.message.chat.id, part, disable_web_page_preview=True)
            else:
                bot.send_message(callback.message.chat.id, game_top1, disable_web_page_preview=True)

        except Exception as e:
            bot.send_message(callback.message.chat.id, f"❌ Произошла ошибка: {str(e)}")

    # Добавьте обработчики для других кнопок
    elif callback.data == "top_discount":
        bot.answer_callback_query(callback.id, "Функция в разработке")
        bot.send_message(callback.message.chat.id, "⚠️ Функция 'Со скидками' скоро будет доступна!")

    elif callback.data == "top_free":
        bot.answer_callback_query(callback.id, "Функция в разработке")
        bot.send_message(callback.message.chat.id, "⚠️ Функция 'Бесплатные' скоро будет доступна!")


bot.polling()

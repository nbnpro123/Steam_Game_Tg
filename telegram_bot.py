from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import telebot
from steam_parser import get_top_games, get_discount_games, get_free_games

bot = telebot.TeleBot(token='8304089254:AAFU7vaP8KxgXiCc5VL591P6JNaOR-gIbXc')


@bot.message_handler(commands=['start'])
def cmd_start(message):
    """Обработчик команды /start"""
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

    bot.send_message(
        message.chat.id,
        welcome_text,
        parse_mode='Markdown',
        reply_markup=keyboard
    )


@bot.message_handler(commands=['help'])
def cmd_help(message):
    """Обработчик команды /help"""
    help_text = (
        "📖 *Помощь по использованию бота*\n\n"
        "*Доступные команды:*\n"
        "• /start - Главное меню\n"
        "• /top - Топ-10 игр по продажам\n"
        "• /discount - Топ-10 игр со скидками\n"
        "• /free - Топ бесплатных игр\n"
        "• /help - Это сообщение\n\n"
        "*Как использовать:*\n"
        "1. Нажмите на одну из кнопок в меню\n"
        "2. Или введите команду вручную\n"
        "3. Бот покажет актуальную информацию из Steam\n\n"
        "⚠️ *Примечание:* Данные обновляются в реальном времени и могут загружаться до 30 секунд."
    )

    bot.send_message(
        message.chat.id,
        help_text,
        parse_mode='Markdown'
    )


@bot.message_handler(commands=['top'])
def send_top_games(message):
    """Обработчик команды /top"""
    try:
        bot.send_message(message.chat.id, "🔄 Получаю актуальный топ игр с Steam...")
        game_top1 = get_top_games()

        # Разбиваем длинное сообщение на части, если оно слишком длинное
        if len(game_top1) > 4000:
            parts = [game_top1[i:i + 4000] for i in range(0, len(game_top1), 4000)]
            for part in parts:
                bot.send_message(message.chat.id, part, parse_mode='Markdown', disable_web_page_preview=True)
        else:
            bot.send_message(message.chat.id, game_top1, parse_mode='Markdown', disable_web_page_preview=True)

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Произошла ошибка: {str(e)}")


@bot.message_handler(commands=['discount'])
def send_discount_games(message):
    """Обработчик команды /discount"""
    try:
        bot.send_message(message.chat.id, "🔄 Ищу игры со скидками...")
        discount_games = get_discount_games()

        if len(discount_games) > 4000:
            parts = [discount_games[i:i + 4000] for i in range(0, len(discount_games), 4000)]
            for part in parts:
                bot.send_message(message.chat.id, part, parse_mode='Markdown', disable_web_page_preview=True)
        else:
            bot.send_message(message.chat.id, discount_games, parse_mode='Markdown', disable_web_page_preview=True)

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Произошла ошибка: {str(e)}")


@bot.message_handler(commands=['free'])
def send_free_games(message):
    """Обработчик команды /free"""
    try:
        bot.send_message(message.chat.id, "🔄 Ищу бесплатные игры...")
        free_games = get_free_games()

        if len(free_games) > 4000:
            parts = [free_games[i:i + 4000] for i in range(0, len(free_games), 4000)]
            for part in parts:
                bot.send_message(message.chat.id, part, parse_mode='Markdown', disable_web_page_preview=True)
        else:
            bot.send_message(message.chat.id, free_games, parse_mode='Markdown', disable_web_page_preview=True)

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Произошла ошибка: {str(e)}")


@bot.callback_query_handler(func=lambda call: True)
def callback_message(callback):
    if callback.data == "top_game":
        bot.answer_callback_query(callback.id, "Загружаю топ игр...")
        bot.send_message(callback.message.chat.id, "Минуточку...")
        try:
            game_top1 = get_top_games()

            if len(game_top1) > 4000:
                parts = [game_top1[i:i + 4000] for i in range(0, len(game_top1), 4000)]
                for part in parts:
                    bot.send_message(callback.message.chat.id, part, parse_mode='Markdown',
                                     disable_web_page_preview=True)
            else:
                bot.send_message(callback.message.chat.id, game_top1, parse_mode='Markdown',
                                 disable_web_page_preview=True)

        except Exception as e:
            bot.send_message(callback.message.chat.id, f"❌ Произошла ошибка: {str(e)}")

    elif callback.data == "top_discount":
        bot.answer_callback_query(callback.id, "Ищу игры со скидками...")
        bot.send_message(callback.message.chat.id, "Минуточку...")
        try:
            discount_games = get_discount_games()

            if len(discount_games) > 4000:
                parts = [discount_games[i:i + 4000] for i in range(0, len(discount_games), 4000)]
                for part in parts:
                    bot.send_message(callback.message.chat.id, part, parse_mode='Markdown',
                                     disable_web_page_preview=True)
            else:
                bot.send_message(callback.message.chat.id, discount_games, parse_mode='Markdown',
                                 disable_web_page_preview=True)

        except Exception as e:
            bot.send_message(callback.message.chat.id, f"❌ Произошла ошибка: {str(e)}")

    elif callback.data == "top_free":
        bot.answer_callback_query(callback.id, "Ищу бесплатные игры...")
        bot.send_message(callback.message.chat.id, "Минуточку...")
        try:
            free_games = get_free_games()

            if len(free_games) > 4000:
                parts = [free_games[i:i + 4000] for i in range(0, len(free_games), 4000)]
                for part in parts:
                    bot.send_message(callback.message.chat.id, part, parse_mode='Markdown',
                                     disable_web_page_preview=True)
            else:
                bot.send_message(callback.message.chat.id, free_games, parse_mode='Markdown',
                                 disable_web_page_preview=True)

        except Exception as e:
            bot.send_message(callback.message.chat.id, f"❌ Произошла ошибка: {str(e)}")

    elif callback.data == "refresh":
        bot.answer_callback_query(callback.id, "Обновляю меню...")
        cmd_start(callback.message)

    elif callback.data == "help":
        bot.answer_callback_query(callback.id, "Показываю помощь...")
        cmd_help(callback.message)


if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)
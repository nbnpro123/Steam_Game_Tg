import telebot
from steam_parser import review_score

bot = telebot.TeleBot(token='8304089254:AAFU7vaP8KxgXiCc5VL591P6JNaOR-gIbXc')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'оценка кс го {review_score}')















bot.polling()
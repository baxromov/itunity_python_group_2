import telebot
import logging
from config import BOT_TOKEN
logging.basicConfig(level=logging.INFO)
TOKEN = BOT_TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    print(message)
    logging.info(message)
    pass


def main():
    bot.polling()

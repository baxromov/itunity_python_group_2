import telebot
import logging
from config import BOT_TOKEN
from db import MySQLConnection

logging.basicConfig(level=logging.INFO)
TOKEN = BOT_TOKEN

bot = telebot.TeleBot(TOKEN)
db = MySQLConnection()


@bot.message_handler(commands=['start'])
def start(message):
    username = f"{message.from_user.first_name} {message.from_user.last_name}"
    bot.send_message(message.from_user.id, f"Hello {username}, What is your first name?")
    bot.register_next_step_handler(message, get_first_name)


def get_first_name(message):
    first_name = message.text
    student = db.create('student', first_name=first_name)
    print(student)
    bot.send_message(message.from_user.id, f"Thanks {message.text}!!! What is your last name?")
    bot.register_next_step_handler(message, get_last_name)


def get_last_name(message):
    bot.send_message(message.chat.id, "Complete!!!")




def main():
    bot.polling()

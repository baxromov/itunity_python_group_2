import datetime

import telebot
import logging

from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from config import BOT_TOKEN
from db import MySQLConnection
from utils import Validations

logging.basicConfig(level=logging.INFO)
TOKEN = BOT_TOKEN

bot = telebot.TeleBot(TOKEN)
db = MySQLConnection()


@bot.message_handler(commands=['start'])
def start(message):
    user_id, is_created = db.get_or_create('student', chat_id=message.chat.id)
    print(message)
    print(is_created)
    username = f"{message.from_user.first_name} {message.from_user.last_name}"
    bot.send_message(message.from_user.id, f"Hello {username}, What is your first name?")
    bot.register_next_step_handler(message, get_first_name)


def get_first_name(message):
    user_id, is_created = db.get_or_create('student', chat_id=message.chat.id)
    first_name = message.text
    db.update('student', _id=user_id[0], first_name=first_name)
    bot.send_message(message.from_user.id, f"Thanks {message.text}!!! What is your last name?")
    bot.register_next_step_handler(message, get_last_name)


def get_last_name(message):
    user_id, is_created = db.get_or_create('student', chat_id=message.chat.id)
    last_name = message.text
    db.update('student', _id=user_id[0], last_name=last_name)
    bot.send_message(message.chat.id, "What is your birthdate? ❗️(dd.mm.yyyy)")
    bot.register_next_step_handler(message, get_birthdate)


def birth_valid(message):
    bot.send_message(message.chat.id, "Please enter a valid date")
    bot.register_next_step_handler(message, get_birthdate)


def get_birthdate(message):
    user_id, is_created = db.get_or_create('student', chat_id=message.chat.id)
    birthdate = message.text
    validate = Validations().validate_date(birthdate)
    if validate:
        birth_date = datetime.datetime.strptime(birthdate, '%d.%m.%Y').date()
        db.update('student', _id=user_id[0], birth_date=birth_date)
        rkm = ReplyKeyboardMarkup(resize_keyboard=True)
        phone = KeyboardButton("Phone number", request_contact=True)
        rkm.add(phone)
        bot.send_message(message.chat.id, "☎️ What is your phone number? ❗(+998901234567)", reply_markup=rkm)
        bot.register_next_step_handler(message, get_phone_number)
    else:
        birth_valid(message)


def get_phone_number(message):
    user_id, is_created = db.get_or_create('student', chat_id=message.chat.id)
    phone_number = message.contact.phone_number
    validate = Validations().validate_phone_number(phone_number)
    if validate:
        db.update('student', _id=user_id[0], phone=phone_number)
        bot.send_message(message.chat.id, "What is your email?")
        bot.register_next_step_handler(message, get_email)
    else:
        bot.send_message(message.chat.id, "Please enter a valid phone number")
        bot.register_next_step_handler(message, get_phone_number)


def get_email(message):
    user_id, is_created = db.get_or_create('student', chat_id=message.chat.id)
    email = message.text
    validate = Validations().validate_email(email)
    if validate:
        db.update('student', _id=user_id[0], email=email)
        bot.send_message(message.chat.id, "What is your address?")
        bot.register_next_step_handler(message, get_address)
    else:
        bot.send_message(message.chat.id, "Please enter a valid email")
        bot.register_next_step_handler(message, get_email)


def get_address(message):
    user_id, is_created = db.get_or_create('student', chat_id=message.chat.id)
    address = message.text
    db.update('student', _id=user_id[0], address=address)
    rkm = ReplyKeyboardMarkup(resize_keyboard=True)
    rkm.row('Male', 'Female')
    bot.send_message(message.chat.id, "What is your gender?", reply_markup=rkm)
    bot.register_next_step_handler(message, get_gender)


def get_gender(message):
    user_id, is_created = db.get_or_create('student', chat_id=message.chat.id)
    gender = message.text
    db.update('student', _id=user_id[0], gender=gender)
    rkm = ReplyKeyboardMarkup(resize_keyboard=True)
    rkm.add("/start")
    bot.send_message(message.chat.id, "Thanks for applying data, we will contact you soon, wait ❗❗❗")
    finish(message)


def finish(message):
    rkm = ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Thank you for applying data, we will contact you soon, wait ❗❗❗",
                     reply_markup=rkm)


def main():
    bot.polling()

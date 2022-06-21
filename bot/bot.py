from aiogram import Bot, Dispatcher, executor
from config import BOT_TOKEN
import logging

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def start_bot(message):
    await message.reply(message.text)


def main():
    executor.start_polling(dp, skip_updates=True)


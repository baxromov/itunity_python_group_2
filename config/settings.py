import os
from dotenv import dotenv_values

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ENV = dotenv_values(os.path.join(BASE_DIR, ".env"))

db_config = {
    "HOST": ENV.get('HOST'),
    "PORT": ENV.get('PORT'),
    "USER": ENV.get("USER"),
    "PASSWORD": ENV.get("PASSWORD"),
    "DB_NAME": ENV.get("DB_NAME")
}


BOT_TOKEN = ENV.get("BOT_TOKEN")

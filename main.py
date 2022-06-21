from connections import MySQLConnection
from config import db_config

if __name__ == "__main__":
    mysql = MySQLConnection(
        host=db_config.get('HOST', "127.0.0.1"),
        user=db_config.get('USER'),
        password=db_config.get('PASSWORD', ''),
        db_name=db_config.get('DB_NAME'),
        port=db_config.get('PORT')
    )

    print(mysql.update("course", _id=8, name="Ingliz tili", description="60 kunda IELTS 9"))
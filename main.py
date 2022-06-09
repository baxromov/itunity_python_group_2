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
    print(mysql.show_table)
    mysql.create(
        table_name='course',
        name="Python",
        description="Oylik 5000$ topmoqchimisiz",
    )

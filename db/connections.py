from mysql import connector
from typing import Optional, Union

from config import db_config


class MySQLConnection:
    """
        MySQL Connection
    """

    def __init__(self):
        self.host = db_config.get('HOST')
        self.port = db_config.get('PORT')
        self.user = db_config.get('USER')
        self.password = db_config.get('PASSWORD')
        self.db_name = db_config.get('DB_NAME')
        self.cnx = connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.db_name
        )

    def is_connection(self) -> Optional[bool]:
        """
        Connection check
        :return:
        """
        return self.cnx.is_connected()

    def connection(self) -> Optional[str]:
        """
        Connection messages
        :return: str
        """
        return f"Connection has been success!" if self.is_connection() else "failed!"

    @property
    def show_table(self) -> Union[list, None]:
        """
        Show tables
        :return:
        """
        cmd = self.cnx.cursor()
        cmd.execute('show tables')
        if cmd:
            return [i for i in cmd]
        else:
            return None

    def describe_table(self, table_name: str):
        """
        Describe table information
        :param table_name:
        :return:
        """
        cmd = self.cnx.cursor()
        cmd.execute(f'describe {table_name}')
        return cmd.description

    def create(self, table_name: str, **kwargs):

        """
        Create records on tables
        :param table_name: table name as staff
        :param kwargs: fields name
        :return:
        """
        if len(tuple(kwargs.values())) == 1:
            cmd = self.cnx.cursor()
            before_values = f"insert into {table_name} {tuple(kwargs.keys())} value".replace("'", '`')
            after_values = tuple(kwargs.values())
            query = f"{before_values} {after_values}".replace(",", "")
            cmd.execute(query)
            self.cnx.commit()
            return cmd
        else:
            cmd = self.cnx.cursor()
            before_values = f"insert into {table_name} {tuple(kwargs.keys())} value".replace("'", '`')
            after_values = tuple(kwargs.values())
            query = f"{before_values} {after_values}"
            cmd.execute(query)
            self.cnx.commit()
            print("Records created !!!")
            return cmd

    def all(self, table_name: str) -> Optional[list]:
        cmd = self.cnx.cursor()
        query = f"select * from {table_name}"
        cmd.execute(query)
        return [item for item in cmd]

    def get(self, table_name: str, **kwargs) -> Union[tuple, None]:
        cmd = self.cnx.cursor()
        right_side_query = ''
        left_side_query = f"select * from {table_name} where "
        for key, value in kwargs.items():
            if isinstance(value, int):
                right_side_query += f"{key}={value} and "
            else:
                right_side_query += f"{key}='{value}' and "

        result = "and".join(right_side_query.strip().split("and")[:-1])
        cmd.execute(left_side_query + result)
        data = cmd.fetchall()
        if len(data) > 1:
            raise ValueError("Get more than one objects")
        else:
            return data[0] if data else None

    def filter(self, table_name: str, **kwargs) -> Optional[list]:
        cmd = self.cnx.cursor()
        right_side_query = ''
        left_side_query = f"select * from {table_name} where "
        for key, value in kwargs.items():
            if isinstance(value, int):
                right_side_query += f"{key}={value} and "
            else:
                right_side_query += f"{key}='{value}' and "
        result = "and".join(right_side_query.strip().split("and")[:-1])
        cmd.execute(left_side_query + result)
        data = cmd.fetchall()
        return data

    def delete(self, table_name: str, **kwargs) -> Optional[str]:
        data = self.get(table_name, **kwargs)[0]
        data_id = data
        query = f"delete from {table_name} where id={data_id}"
        self.cnx.cursor().execute(query)
        self.cnx.commit()
        return f"{data_id} is deleted!!!"

    def update(self, table_name: str, _id: int, **kwargs) -> Optional[tuple]:
        cmd = self.cnx.cursor()
        left_side = f"update {table_name} set "
        middle_side = ""
        for k, v in kwargs.items():
            if isinstance(v, int):
                middle_side += f"{k}={v}, "
            else:
                middle_side += f"{k}='{v}', "
        result = ",".join(middle_side.strip().split(",")[:-1])
        right_side = f"where id={_id}"
        cmd.execute(left_side + result + right_side)
        self.cnx.commit()
        data = self.get(table_name, id=_id)
        return data

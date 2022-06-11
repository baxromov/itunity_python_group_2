from mysql import connector
from typing import Optional, Union


class MySQLConnection:
    """
        MySQL Connection
    """

    def __init__(self,
                 host,
                 port: Optional[None],
                 user,
                 password,
                 db_name):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db_name = db_name
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

    def create(self, table_name, **kwargs):

        """
        Create records on tables
        :param table_name: table name as staff
        :param kwargs: fields name
        :return:
        """
        cmd = self.cnx.cursor()
        before_values = f"insert into {table_name} {tuple(kwargs.keys())} value".replace("'", '`')
        after_values = f"{tuple(kwargs.values())}"
        query = f"{before_values} {after_values}"
        cmd.execute(query)
        self.cnx.commit()
        print("Records created !!!")
        return cmd

    def all(self, table_name):
        cmd = self.cnx.cursor()
        query = f"select * from {table_name}"
        cmd.execute(query)
        return [item for item in cmd]

    def get(self, table_name, **kwargs):
        cmd = self.cnx.cursor()

        query = f"select * from {table_name} where {tuple(kwargs.keys())[0]}={tuple(kwargs.values())[0]}".replace("'", "")
        # print(query)
        cmd.execute(query)

    def update(self):
        pass

    def delete(self):
        pass

    def filter(self):
        pass

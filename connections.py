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
        self.cursor = self.cnx.cursor()

    def is_connection(self) -> Optional[bool]:
        """
        Connection check
        :return:
        """
        return self.cnx.is_connected()

    def connection(self) -> Optional[str]:
        """
        Connection messages
        :return:
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




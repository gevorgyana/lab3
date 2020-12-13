import psycopg2

class DBConnectionInfo:
    def __init__(self, dbname: str, host: str, password: str, user: str):
        self.dbname = dbname
        self.host = host
        self.password = password
        self.user = user
        self.port = 5432

class Py2SQL:
    __connection = None

    @staticmethod
    def db_connect(db: DBConnectionInfo):
        Py2SQL.__connection = psycopg2.connect(
            dbname=db.dbname,
            user=db.user,
            host=db.host,
            password=db.password
        )

    def db_disconnect():
        Py2SQL.__connection.close()

    def db_engine():
        """
        Examples:
        >>> print(1)

        """
        cur = Py2SQL.__connection.cursor()
        cur.execute("select version();")
        cur.close()
        return cur.fetchone()[0].split(' ')[:2]

if __name__ == "__main__":
    db_config = DBConnectionInfo("test", "localhost", "adminadminadmin", "postgres")
    Py2SQL.db_connect(db_config)
    print(Py2SQL.db_engine())
    Py2SQL.db_disconnect()

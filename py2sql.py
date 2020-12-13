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
            >>> name, version = Py2SQL.db_engine()

        """
        cur = Py2SQL.__connection.cursor()
        cur.execute("select version();")
        retval = cur.fetchone()[0].split(' ')[:2]
        cur.close()
        return retval

    def db_name():
        cur = Py2SQL.__connection.cursor()
        cur.execute("select current_database();")
        retval = cur.fetchone()[0]
        cur.close()
        return retval

if __name__ == "__main__":
    db_config = DBConnectionInfo("test", "localhost", "adminadminadmin", "postgres")
    Py2SQL.db_connect(db_config)
    name, ver = Py2SQL.db_engine()
    print(name, ver)
    print(Py2SQL.db_name())
    Py2SQL.db_disconnect()

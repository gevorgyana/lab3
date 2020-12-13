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

    @staticmethod
    def db_disconnect():
        Py2SQL.__connection.close()

    @staticmethod
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

    @staticmethod
    def db_name():
        cur = Py2SQL.__connection.cursor()
        cur.execute("select current_database();")
        retval = cur.fetchone()[0]
        cur.close()
        return retval

    @staticmethod
    def db_size():
        db_name = Py2SQL.db_name()
        cur = Py2SQL.__connection.cursor()
        # attention - no double quotes!
        string_cmd = "select pg_size_pretty( pg_database_size('{}') );".format(db_name)
        cur.execute(string_cmd)
        retval = cur.fetchone()[0]
        cur.close()
        return retval

    @staticmethod
    def db_tables():
        db_name = Py2SQL.db_name()
        cur = Py2SQL.__connection.cursor()
        string_cmd = "select * from pg_catalog.pg_tables where schemaname != 'pg_catalog' and schemaname != 'information_schema';"
        cur.execute(string_cmd)
        retval = cur.fetchone()
        cur.close()
        return retval

    @staticmethod
    def db_table_structure(table):
        cur = Py2SQL.__connection.cursor()
        string_cmd = "select column_name, data_type from information_schema.columns where table_name = '{}'".format(table)
        cur.execute(string_cmd)
        retval = cur.fetchall()
        cur.close()
        retval = [(i, attr[0], attr[1]) for i, attr in enumerate(retval)]
        return retval

if __name__ == "__main__":
    db_config = DBConnectionInfo("test", "localhost", "adminadminadmin", "postgres")
    Py2SQL.db_connect(db_config)
    Py2SQL.db_table_structure("pg_settings")
    Py2SQL.db_disconnect()

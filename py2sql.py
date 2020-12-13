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
        """Works
        """
        Py2SQL.__connection = psycopg2.connect(
            dbname=db.dbname,
            user=db.user,
            host=db.host,
            password=db.password
        )

    @staticmethod
    def db_disconnect():
        """Works
        """
        Py2SQL.__connection.close()

    @staticmethod
    def db_engine():
        """Works
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
        """Works
        """
        cur = Py2SQL.__connection.cursor()
        cur.execute("select current_database();")
        retval = cur.fetchone()[0]
        cur.close()
        return retval

    @staticmethod
    def db_size():
        """Works
        """
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
        """It works
        """
        db_name = Py2SQL.db_name()
        cur = Py2SQL.__connection.cursor()
        # All tables that exist in the system can be obtained,
        # By default, there are 2 table schemas (databases),
        # they are `information_schema` and `pg_catalog`.
        #
        # We should of course filter the results to only show the
        # tables that belong to the user's schema (database). Hence the
        # `where`-clause.
        string_cmd = "select * from information_schema.tables where table_schema = '{}' ;".format(Py2SQL.db_name())
        cur.execute(string_cmd)
        retval = [(i[1], i[2]) for i in cur.fetchall()]
        cur.close()
        return retval

    @staticmethod
    def db_table_structure(table):
        """Works
        """
        cur = Py2SQL.__connection.cursor()
        string_cmd = "select column_name, data_type from information_schema.columns where table_name = '{}'".format(table)
        cur.execute(string_cmd)
        retval = cur.fetchall()
        cur.close()
        # We have to flatten data because of the indices that have been
        # artificially added to enumerate the attributes.
        retval = tuple([(i, attr[0], attr[1]) for i, attr in enumerate(retval)])
        return retval

    @staticmethod
    def db_table_size(table):
        pass
    """
        cur = Py2SQL.__connection.cursor()
        string_cmd = "select pg_size_pretty( pg_total_relation_size('{}') );".format(table)
        cur.execute(string_cmd)
        # retval = cur.fetchone()[0]
        retval = cur.fetchall()
        print(retval)

        cur.close()
        return retval
"""

if __name__ == "__main__":
    db_config = DBConnectionInfo("test", "localhost", "adminadminadmin", "postgres")
    Py2SQL.db_connect(db_config)

    # print(Py2SQL.db_table_size("pg_settings"))
    Py2SQL.db_disconnect()

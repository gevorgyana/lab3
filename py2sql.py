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
            password=db.password,
            port=db.port
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
        # string_cmd = "select pg_size_pretty( pg_database_size('{}') );".format(db_name)
        string_cmd = "select pg_database_size('{}');".format(db_name)
        cur.execute(string_cmd)
        retval = int(cur.fetchone()[0]) / 1024 / 1024
        cur.close()
        return retval

    @staticmethod
    def db_tables():
        """Works
        """
        db_name = Py2SQL.db_name()
        cur = Py2SQL.__connection.cursor()

        # By default, there are 2 table schemas (databases),
        # they are `information_schema` and `pg_catalog`.
        #
        # We should of course filter the results to only show the
        # tables that belong to the user's schema (database). Hence the
        # `where`-clause.
        # By default, new tables are put in `default` schema, but it is
        # not clever to rely on this, it would be better to filter out
        # the schemas coming from PostgreSQL.
        #
        # Reference: https://www.postgresql.org/docs/9.1/infoschema-tables.html
        string_cmd = "select table_name from information_schema.tables where table_schema != 'pg_catalog' and table_schema != 'information_schema' order by table_name;"
        cur.execute(string_cmd)
        retval = [i[0] for i in cur.fetchall()]
        cur.close()
        # Returns only one element, no no filtering is required
        return retval

    @staticmethod
    def db_table_structure(table):
        """Works
        Reference: https://www.postgresql.org/docs/current/information-schema.html
        """
        cur = Py2SQL.__connection.cursor()
        string_cmd = "select column_name, data_type from information_schema.columns where table_name = '{}' and table_schema != 'information_schema' and table_schema != 'pg_catalog'".format(table)
        cur.execute(string_cmd)
        retval = cur.fetchall()
        cur.close()
        retval = tuple([(i, attr[0], attr[1]) for i, attr in enumerate(retval)])
        return retval

    @staticmethod
    def db_table_size(table):
        cur = Py2SQL.__connection.cursor()
        string_cmd = "select pg_total_relation_size('{}');".format(table)
        cur.execute(string_cmd)
        retval = int(cur.fetchone()[0]) / 1024 / 1024
        print(retval)
        cur.close()
        return retval

if __name__ == "__main__":
    # This code thinks that init code was already run from the
    # test/main.go source file
    db_config = DBConnectionInfo("test", "localhost", "adminadminadmin", "postgres")
    Py2SQL.db_connect(db_config)
    Py2SQL.db_disconnect()

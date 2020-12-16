import psycopg2
import inspect
import pickle
import codecs

DEBUG = False
DEBUG = True

def log(*msg):
    if DEBUG:
        print(*msg)

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
            password=db.password,
            port=db.port
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
        string_cmd = "select version();"
        log("executing:", string_cmd)
        cur.execute(string_cmd)
        retval = cur.fetchone()[0].split(' ')[:2]
        log("retval:", retval)
        cur.close()
        return retval

    @staticmethod
    def db_name():
        cur = Py2SQL.__connection.cursor()
        string_cmd = "select current_database();"
        log("executing:", string_cmd)
        cur.execute(string_cmd)
        retval = cur.fetchone()[0]
        log("retval:", retval)
        cur.close()
        return retval

    @staticmethod
    def db_size():
        db_name = Py2SQL.db_name()
        cur = Py2SQL.__connection.cursor()
        # Attention - no double quotes!
        string_cmd = "select pg_database_size('{}');".format(db_name)
        log("executing:", string_cmd)
        cur.execute(string_cmd)
        retval = int(cur.fetchone()[0]) / 1024 / 1024
        log("retval:", retval)
        cur.close()
        return retval

    @staticmethod
    def db_tables():
        db_name = Py2SQL.db_name()
        cur = Py2SQL.__connection.cursor()

        # By default, there are 2 table schemas (databases),
        # (`information_schema` and `pg_catalog`) that store metadata.
        #
        # We should of course filter the results to only show the
        # tables that belong to the user's schema (database). Hence the
        # `where`-clause.
        #
        # By default, new tables are put in `default` schema, but it is
        # not clever to rely on this, it would be better to filter out
        # the schemas coming from PostgreSQL.
        #
        # Reference: https://www.postgresql.org/docs/9.1/infoschema-tables.html
        string_cmd = "select table_name from information_schema.tables where table_schema != 'pg_catalog' and table_schema != 'information_schema' order by table_name;"
        log("executing:", string_cmd)
        cur.execute(string_cmd)
        retval = [i[0] for i in cur.fetchall()]
        log("retval:", retval)
        cur.close()
        return retval

    @staticmethod
    def db_table_structure(table):
        cur = Py2SQL.__connection.cursor()
        # Reference: https://www.postgresql.org/docs/current/information-schema.html
        string_cmd = "select column_name, data_type from information_schema.columns where table_name = '{}' and table_schema != 'information_schema' and table_schema != 'pg_catalog' order by column_name".format(table)
        log("executing:", string_cmd)
        cur.execute(string_cmd)
        retval = cur.fetchall()
        cur.close()
        retval = [(i, attr[0], attr[1]) for i, attr in enumerate(retval)]
        log("retval:", retval)
        return retval

    @staticmethod
    def db_table_size(table):
        cur = Py2SQL.__connection.cursor()
        string_cmd = "select pg_total_relation_size('{}');".format(table)
        log("executing:", string_cmd)
        cur.execute(string_cmd)
        retval = int(cur.fetchone()[0]) / 1024 / 1024
        log("retval:", retval)
        cur.close()
        return retval

    @staticmethod
    def drop_table(table_name):
        cur = Py2SQL.__connection.cursor()
        cur.execute("drop table if exists {};".format(table_name))
        cur.close()
        Py2SQL.__connection.commit()

    @staticmethod
    def save_class(class_):
        """Populates the database with the representation of a class, by
        reading its columns. Does not try to create a table with a duplicate
        name.

        Examples:
            >>> class Foo:
            >>>     value str
            >>> foo = Foo
            >>> Py2SQL.save_class(foo)
        """
        Py2SQL.__save_class_with_foreign_key(class_, [])

    @staticmethod
    def __save_class_with_foreign_key(class_, parents):
        cur = Py2SQL.__connection.cursor()
        cur.execute("drop table if exists {};".format(class_.__name__))
        annotated_data = None
        for t in inspect.getmembers(class_, lambda a:not(inspect.isroutine(a))):
            if t[0] == "__annotations__":
                annotated_data = t[1]
                # `serial` is autoincremented!
        string_cmd = "create table if not exists {} (id serial primary key not null, ".format(class_.__name__)

        # Connect to already existing parent tables.
        for p in parents:
            parent_name = p.__name__
            string_cmd += f"{parent_name}_id serial references {parent_name} (id), "

        for i in annotated_data.keys():
            string_cmd += "{} bytea, ".format(i)

        string_cmd = string_cmd[:-2]
        string_cmd += ");"
        log("executing:", string_cmd)
        cur.execute(string_cmd)
        cur.close()
        Py2SQL.__connection.commit()

    @staticmethod
    def save_object(object_):
        """Inserts data into the database named after the class name of the object.
        TODO ASK check if it exists - how?? Got it now. Set private id of object.
        TODO Need to catch an exception for when a table is not created yet
        """
        table_name = type(object_).__name__
        annotated_data = None
        for t in inspect.getmembers(object_, lambda a:not(inspect.isroutine(a))):
            if t[0] == "__annotations__":
                annotated_data = t[1]
        cur = Py2SQL.__connection.cursor()

        specific_columns = ""
        for i in annotated_data.keys():
            specific_columns += str(i)
            specific_columns += ","
        specific_columns = specific_columns[:-1]
        print("COLUMNS", specific_columns)

        string_cmd = "insert into {} ({}) values (".format(table_name, specific_columns)
        log("THIS IS IT", object_.__dict__)
        attr_values = []
        for i in annotated_data.keys():
            attr_values.append(pickle.dumps(object_.__dict__[i]))
            string_cmd += "%s , ".format(pickle.dumps(object_.__dict__[i]))
        string_cmd = string_cmd[:-2]
        string_cmd += ");"
        log("executing:", string_cmd)
        cur.execute(string_cmd, tuple(attr_values))
        cur.close()
        Py2SQL.__connection.commit()
        # foo
        cur = Py2SQL.__connection.cursor()
        cur.execute("select * from s;")
        print(cur.fetchall())
        cur.close()

    """
    @staticmethod
    def save_hierarchy(root_class):
        q = [root_class]
        while len(q) > 0:
            log("list log 1:", q)
            front = q.pop()
            if front == object:
                log("stop")
                break
            Py2SQL.__save_class_with_foreign_key(front, front.__bases__)
            q = [*q, *list(front.__bases__)]
    """


class S:
    foo: int
    bar: int
    def __init__(self, foo, bar):
        self.foo = foo
        self.bar = bar

if __name__ == "__main__":
    con = DBConnectionInfo("test", "localhost", "adminadminadmin", "postgres")
    Py2SQL.db_connect(con)
    Py2SQL.save_class(S)
    s = S("one", 1)
    Py2SQL.save_object(s)
    Py2SQL.db_disconnect()

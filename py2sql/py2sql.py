import psycopg2

from dataclasses import dataclass
import inspect
import pickle
import codecs

DEBUG = False
DEBUG = True

"""
TODO
- Delete by content
- Map into user types (not only bytea)
- No hierarchy (only save and delete)
"""

def log(*msg):
    if DEBUG:
        print(*msg)

@dataclass
class DBConnectionInfo:
    """This is a data object that should contain the fileds necessary to connect
    to the underlying database: dbname, host, password, user.
    """
    dbname: str
    host: str
    password: str
    user: str
    port: int = 5432

class Py2SQL:
    __connection = None

    @staticmethod
    def db_connect(db: DBConnectionInfo):
        """
        Parameters
        ----------
        db : DBConnectionInfo
            An object that contains necessary information for connecting to
            the database.
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
        Py2SQL.__connection.close()

    @staticmethod
    def db_engine():
        """
        Returns a tuple that represents the name of the underlying
        database and its version.

        Examples:
        ---------
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
        """Returns the name of the current database.
        """
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
        """Returns the size of the current database.
        """
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
        """Returns the names of the tables that currently exist in the system.
        This method does not respect the system tables (`information_schema` & `pg*`).
        """
        db_name = Py2SQL.db_name()
        cur = Py2SQL.__connection.cursor()
        # Reference: https://www.postgresql.org/docs/9.1/infoschema-tables.html
        string_cmd = "select table_name from information_schema.tables where table_schema not like 'pg_%' and table_schema != 'information_schema' order by table_name;"
        log("executing:", string_cmd)
        cur.execute(string_cmd)
        retval = [i[0] for i in cur.fetchall()]
        log("retval:", retval)
        cur.close()
        return retval

    @staticmethod
    def db_table_structure(table):
        """
        Returns a list describing the structure of the database. Each list element is
        a tuple of the following king: (column_number, column_name, column_type).

        Parameters
        ----------
        table : table name of user's interest.
        """
        cur = Py2SQL.__connection.cursor()
        # Reference: https://www.postgresql.org/docs/current/information-schema.html
        string_cmd = "select column_name, data_type from information_schema.columns where table_name = '{}' and table_schema != 'information_schema' and table_schema not like 'pg%' order by column_name".format(table)
        log("executing:", string_cmd)
        cur.execute(string_cmd)
        retval = cur.fetchall()
        cur.close()
        retval = [(i, attr[0], attr[1]) for i, attr in enumerate(retval)]
        log("retval:", retval)
        return retval

    @staticmethod
    def db_table_size(table):
        """Returns the size of the table.

        Parameters
        ----------
        table : table name of user's interest.
        """
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
        """Drops the table. This should not be exported to the user,
        as this only runs in unit tests. But it can't be done, as unit tests
        rely on this method. So it remains here.

        Parameters
        ----------
        table_name : table name of user's interest.
        """
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
        ---------
            >>> class Foo:
            >>>     value str
            >>> foo = Foo
            >>> Py2SQL.save_class(foo)
        """
        Py2SQL.__save_class_with_foreign_key(class_, [])

    @staticmethod
    def __save_class_with_foreign_key(class_, parents):
        """This is private method that contains the logic of creating
        a PostgreSQL table with the foreign keys defined by parents. This method
        uses reflection to check annotated attributes of the class and decide
        the layout of the to-be-created table.

        Parameters
        ----------
        class_ : the class that should be mapped onto the database.

        parents : the classes that are considered as foreign to this class. That is,
        these classes should be its parents and contain data that complements the
        objects of type class_.
        """
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
        """Writes a representation of the object to the database. It looks at the
        object't underlying type (via reflection) to decide where to write the object.
        This function uses the annotated attributes of the object's type to decide
        what data to store in the database (columns).

        Parameters
        ----------
        object_ : the object whose representation should appear in the database.

        Raises
        ------
        NotImplementedError
            If save_class() has not been previously called, then this method does not
            find the corresponding table and raises the exception.
        """
        table_name = type(object_).__name__
        cur = Py2SQL.__connection.cursor()
        # UNIT_CORNER 1 more unit test case: check if a table is already there
        table_exists = cur.execute("select exists (select * from information_schema.tables where table_name = %s)", ('',))
        if cur.fetchone()[0] == False:
            raise NotImplementedError("This ORM requires a user to run save_class() before running save_object()")
        annotated_data = None
        for t in inspect.getmembers(object_, lambda a:not(inspect.isroutine(a))):
            if t[0] == "__annotations__":
                annotated_data = t[1]
        specific_columns = ""
        for i in annotated_data.keys():
            specific_columns += str(i)
            specific_columns += ","
        specific_columns = specific_columns[:-1]
        print("COLUMNS", specific_columns)
        string_cmd = "insert into {} ({}) values (".format(table_name, specific_columns)
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
        cur = Py2SQL.__connection.cursor()
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

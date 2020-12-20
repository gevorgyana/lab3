import unittest
from dataclasses import dataclass
import sys
import os

sys.path.insert(0, os.getcwd())
from py2sql import py2sql


class TestSaveDeleteObject(unittest.TestCase):
    db_name = "test"
    db_config = py2sql.DBConnectionInfo(db_name, "localhost", "adminadminadmin", "postgres")

    @dataclass
    class Foo:
        foo_1: str = "s1"
        foo_2: int = 2

    @dataclass
    class Miss:
        miss: str = "-1"

    @dataclass
    class Foo_der1(Foo):
        der_1: int = 3

    @dataclass
    class Foo_der11(Foo_der1):
        der_11: str = "dd"

    @dataclass
    class Foo_der2(Foo):
        der_2: bool = True

    def test_create_hierarchy(self):
        db_con_info = py2sql.DBConnectionInfo("test", "localhost", "adminadminadmin", "postgres")
        py2sql.Py2SQL.db_connect(db_con_info)

        py2sql.Py2SQL.save_hierarchy(TestSaveDeleteObject.Foo)

        tables = py2sql.Py2SQL.db_tables()
        self.assertTrue("foo" in tables and "foo_der1" in tables and
                        "foo_der11" in tables and "foo_der2" in tables
                        and "miss" not in tables)

        foo_der11_columns = [j for i in py2sql.Py2SQL._select_from_table('foo_der11') for j in i]
        self.assertTrue('id' in foo_der11_columns and 'foo_1' in foo_der11_columns and
                        'foo_2' in foo_der11_columns and 'der_1' in foo_der11_columns and
                        'der_11' in foo_der11_columns)

        foo_der1_columns = [j for i in py2sql.Py2SQL._select_from_table('foo_der1') for j in i]
        self.assertTrue('id' in foo_der1_columns and 'foo_1' in foo_der1_columns and
                        'foo_2' in foo_der1_columns and 'der_1' in foo_der1_columns)

        py2sql.Py2SQL.delete_hierarchy(TestSaveDeleteObject.Foo)

        py2sql.Py2SQL.db_disconnect()

    def test_delete_hierarchy(self):
        db_con_info = py2sql.DBConnectionInfo("test", "localhost", "adminadminadmin", "postgres")
        py2sql.Py2SQL.db_connect(db_con_info)

        py2sql.Py2SQL.save_hierarchy(TestSaveDeleteObject.Foo)
        py2sql.Py2SQL.delete_hierarchy(TestSaveDeleteObject.Foo)
        tables = py2sql.Py2SQL.db_tables()
        self.assertFalse("foo" in tables or "foo_der1" in tables or
                         "foo_der11" in tables or "foo_der2" in tables
                         or "miss" in tables)

        py2sql.Py2SQL.db_disconnect()

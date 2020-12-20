import unittest
from dataclasses import dataclass
import sys
import os
sys.path.insert(0, os.getcwd())
from py2sql import py2sql


class TestSaveDeleteObject(unittest.TestCase):

    db_name = "test"
    db_config = py2sql.DBConnectionInfo(db_name, "localhost", "adminadminadmin", "postgres")

    def test_save_object_with_no_class_raises_exception(self):
        @dataclass
        class Bar:
            done: bool = True
        py2sql.Py2SQL.db_connect(self.db_config)
        b = Bar()
        with self.assertRaises(NotImplementedError):
            py2sql.Py2SQL.save_object(b)
        py2sql.Py2SQL.db_disconnect()
        py2sql.Py2SQL.db_connect(self.db_config)
        py2sql.Py2SQL.delete_class(Bar)
        self.assertEqual([],
            py2sql.Py2SQL.db_table_structure("s")
        )
        py2sql.Py2SQL.db_disconnect()

    def test_save_class_and_object(self):
        py2sql.Py2SQL.db_connect(self.db_config)
        @dataclass
        class S:
            foo: int = 0
            bar: int = 1
        py2sql.Py2SQL.save_class(S)
        s = S("one", 1)
        py2sql.Py2SQL.save_object(s)
        py2sql.Py2SQL.db_disconnect()
        py2sql.Py2SQL.db_connect(self.db_config)
        py2sql.Py2SQL.delete_class(S)
        self.assertEqual([],
            py2sql.Py2SQL.db_table_structure("s")
        )
        py2sql.Py2SQL.db_disconnect()

    def test_save_and_delete(self):
        @dataclass
        class Foo:
            foo: str = "val"

        class Bar(Foo):
            bar: int = 2

        b = Bar()
        b.bar = 42
        b.foo = "new val"

        db_con_info = py2sql.DBConnectionInfo("test", "localhost", "adminadminadmin", "postgres")
        py2sql.Py2SQL.db_connect(db_con_info)
        py2sql.Py2SQL.save_class(Bar)
        py2sql.Py2SQL.save_object(b)
        self.assertTrue("bar" in py2sql.Py2SQL.db_tables())
        py2sql.Py2SQL.delete_object(b)
        py2sql.Py2SQL.delete_class(Bar)
        self.assertTrue("bar" not in py2sql.Py2SQL.db_tables())
        py2sql.Py2SQL.db_disconnect()

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

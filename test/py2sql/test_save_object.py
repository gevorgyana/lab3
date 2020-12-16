import unittest
from dataclasses import dataclass
import sys
import os
sys.path.insert(0, os.getcwd())
from py2sql import py2sql


class TestSaveDeleteObject(unittest.TestCase):

    table_name = "test"
    db_config = py2sql.DBConnectionInfo(table_name, "localhost", "adminadminadmin", "postgres")

    def tearDown(self):
        py2sql.Py2SQL.db_connect(self.db_config)
        py2sql.Py2SQL._drop_table(table_name)
        py2sql.Py2SQL.db_disconnect()

    def save_object_with_no_class_raises_exception():
        py2sql.Py2SQL.db_connect(self.db_config)
        b = Bar()
        py2sql.Py2SQL.save_object(b)
        py2sql.Py2SQL.db_disconnect()

    def save_class_and_object():
        py2sql.Py2SQL.db_connect(self.db_config)

        @dataclass
        class S:
            foo: int = 0
            bar: int = 1

        con = py2sql.DBConnectionInfo(table_name, "localhost", "adminadminadmin", "postgres")
        py2sql.Py2SQL.db_connect(con)
        py2sql.Py2SQL.save_class(S)
        s = S("one", 1)
        py2sql.Py2SQL.save_object(s)
        py2sql.Py2SQL.db_disconnect()

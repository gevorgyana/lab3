import unittest

import unittest
import sys
import os
sys.path.insert(0, os.getcwd())
from py2sql import py2sql


class F(unittest.TestCase):

    db_config = py2sql.DBConnectionInfo("test", "localhost", "adminadminadmin", "postgres")

    def tearDown(self):
        py2sql.Py2SQL.db_connect(self.db_config)
        py2sql.Py2SQL.drop_table("test")
        py2sql.Py2SQL.db_disconnect()

    def save_object_with_no_class_raises_exception():
        py2sql.Py2SQL.db_connect(self.db_config)
        b = Bar()
        py2sql.Py2SQL.save_object(b)
        py2sql.Py2SQL.db_disconnect()

    def save_class_and_object():
        py2sql.Py2SQL.db_connect(self.db_config)

        class S:
            foo: int
            bar: int
            def __init__(self, foo, bar):
                self.foo = foo
                self.bar = bar

        con = py2sql.DBConnectionInfo("test", "localhost", "adminadminadmin", "postgres")
        py2sql.Py2SQL.db_connect(con)
        py2sql.Py2SQL.save_class(S)
        s = S("one", 1)
        py2sql.Py2SQL.save_object(s)
        py2sql.Py2SQL.db_disconnect()

        py2sql.Py2SQL.db_disconnect()

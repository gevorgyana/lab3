import unittest
import sys
import os
sys.path.append('../..')
from py2sql import py2sql

class Sample:
    foo: int
    bar: str
    def __init__(self):
        self.foo = 1
        self.bar = "bar"

class SubSample(Sample):
    zoo: int
    def __init__(self):
        self.zoo = 2

class Bar:
    done: bool
    def __init__(self):
        self.done = True

class TestSaveClass(unittest.TestCase):

    table_name = "test"
    db_config = py2sql.DBConnectionInfo(table_name, "localhost", "adminadminadmin", "postgres")

    def tearDown(self):
        py2sql.Py2SQL.db_connect(self.db_config)
        py2sql.Py2SQL._drop_table(self.table_name)
        py2sql.Py2SQL.db_disconnect()

    def test_save_class_called_twice(self):
        py2sql.Py2SQL.db_connect(self.db_config)
        try:
            py2sql.Py2SQL.save_class(Bar)
            py2sql.Py2SQL.save_class(Bar)
        except:
            self.fail("save_class() should not throw after being called twice.")
        print("DB TABLE STRUCTURE", py2sql.Py2SQL.db_table_structure("bar"))
        py2sql.Py2SQL.db_disconnect()

if __name__ == "__main__":
    unittest.main()
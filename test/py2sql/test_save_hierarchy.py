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

class TestSavingHierarchy(unittest.TestCase):

    db_config = py2sql.DBConnectionInfo("test", "localhost", "adminadminadmin", "postgres")

    def tearDown(self):
        py2sql.Py2SQL.db_connect(self.db_config)
        py2sql.Py2SQL.drop_table("test")
        py2sql.Py2SQL.db_disconnect()

    def test_save_class_normal_usecase(self):
        py2sql.Py2SQL.db_connect(self.db_config)
        py2sql.Py2SQL.save_class(Bar)
        self.assertNotEqual((), py2sql.Py2SQL.db_table_structure("bar"))
        py2sql.Py2SQL.save_class(Bar)
        self.assertNotEqual((), py2sql.Py2SQL.db_table_structure("bar"))
        py2sql.Py2SQL.db_disconnect()

    def test_save_object_normal_usecase(self):
        py2sql.Py2SQL.db_connect(self.db_config)
        b = Bar()
        py2sql.Py2SQL.save_object(b)
        py2sql.Py2SQL.db_disconnect()


if __name__ == "__main__":
    unittest.main()

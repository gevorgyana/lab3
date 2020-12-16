import unittest
from dataclasses import dataclass
import sys
import os
sys.path.append('../..')
from py2sql import py2sql

@dataclass
class Sample:
    foo: int = 0
    bar: str = "bar"

@dataclass
class SubSample(Sample):
    zoo: int = 1

@dataclass
class Bar:
    done: bool = True

class TestClassSaveDelete(unittest.TestCase):

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

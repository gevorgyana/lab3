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

    db_name = "test"
    table_name = "bar"
    db_config = py2sql.DBConnectionInfo(db_name, "localhost", "adminadminadmin", "postgres")

    def test_save_class_called_twice(self):
        py2sql.Py2SQL.db_connect(self.db_config)

        self.assertEqual([],
            py2sql.Py2SQL.db_table_structure("bar")
        )
        try:
            py2sql.Py2SQL.save_class(Bar)
            self.assertEqual([(0, 'id', 'integer'), (1, 'done', 'boolean')],
                py2sql.Py2SQL.db_table_structure("bar")
            )
            py2sql.Py2SQL.save_class(Bar)
        except:
            self.fail("save_class() should not throw after being called twice.")
        self.assertEqual([(0, 'id', 'integer'), (1, 'done', 'boolean')],
                         py2sql.Py2SQL.db_table_structure("bar")
        )

        py2sql.Py2SQL.delete_class(Bar)
        self.assertEqual([],
            py2sql.Py2SQL.db_table_structure("bar")
        )
        py2sql.Py2SQL.db_disconnect()

if __name__ == "__main__":
    unittest.main()

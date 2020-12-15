import unittest
import sys
sys.path.append('../..')
from py2sql import py2sql

class Sample:
    foo: int
    bar: str

class SubSample(Sample):
    zoo: int

class Bar:
    done: bool

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
        py2sql.Py2SQL.db_disconnect()

    """
    def test_save_object_normal_usecase(self):
        # This code thinks that init code was already run from the
        # test/main.go source file
        db_config = py2sql.DBConnectionInfo("test", "localhost", "adminadminadmin", "postgres")
        py2sql.Py2SQL.db_connect(db_config)
        py2sql.Py2SQL.save_class(Bar)
        self.assertNotEqual((), py2sql.Py2SQL.db_table_structure("bar"))
        py2sql.Py2SQL.db_disconnect()
    """

if __name__ == "__main__":
    unittest.main()

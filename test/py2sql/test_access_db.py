import unittest
import sys
import os
sys.path.insert(0, os.getcwd())
from py2sql import py2sql


class TestGeneralAccess(unittest.TestCase):
    db_config = py2sql.DBConnectionInfo("test", "localhost", "adminadminadmin", "postgres")

    def tearDown(self):
        py2sql.Py2SQL.db_connect(self.db_config)
        py2sql.Py2SQL.drop_table("test")
        py2sql.Py2SQL.db_disconnect()

    def run_all_readonly_functions():
        py2sql.Py2SQL.db_connect(self.db_config)
        py2sql.db_engine()
        py2sql.db_name()
        py2sql.db_size()
        py2sql.db_tables()
        py2sql.db_table_structure("test")
        py2sql.db_table_size("test")
        py2sql.Py2SQL.db_disconnect()

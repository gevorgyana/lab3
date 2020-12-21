import unittest
import sys
import os
sys.path.insert(0, os.getcwd())
from py2sql import py2sql


class TestGeneralAccess(unittest.TestCase):
    db_config = py2sql.DBConnectionInfo("test", "localhost", "adminadminadmin", "postgres")

    def tearDown(self):
        py2sql.Py2SQL.db_connect(self.db_config)
        py2sql.Py2SQL._drop_table("test")
        py2sql.Py2SQL.db_disconnect()

    def test_run_all_readonly_functions(self):
        py2sql.Py2SQL.db_connect(self.db_config)
        py2sql.Py2SQL.db_engine()
        py2sql.Py2SQL.db_name()
        py2sql.Py2SQL.db_size()
        py2sql.Py2SQL.db_tables()

        py2sql.Py2SQL._create_table("test", "(id serial primary key not null , foo varchar(100), bar text, zoo bytea)")

        self.assertEqual(
            # serial is really pseudo-type, it is mapped into integer
            [(0, 'id', 'integer'), (1, 'foo', 'character varying'),
             (2, 'bar', 'text'), (3, 'zoo', 'bytea')
            ],
            py2sql.Py2SQL.db_table_structure("test")
        )

        # it is never 0, even with no data
        self.assertGreater(py2sql.Py2SQL.db_table_size("test"), 0)

        py2sql.Py2SQL.db_disconnect()


from Py_to_SQL import *

class TestClass:
    def __init__(self):
        self.a=10
        self.b=123
        self.c=2.21
        self.d="sda"

if __name__ == "__main__":
    # This code thinks that init code was already run from the
    # test/main.go source file
    db_config = DBConnectionInfo("test", "localhost", "adminadminadmin", "postgres")

    Py2SQL.db_connect(db_config)

    PyToSQL.db_save_class(TestClass)
   # PyToSQL.db_delete_class(TestClass)
    test_obj=TestClass()
    test_obj.a=15
    test_obj.d="saasd"
    PyToSQL.db_save_object(test_obj)
    Py2SQL.db_disconnect()

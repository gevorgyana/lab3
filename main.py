
from py2sql_2 import *

class TestClass:
    def __init__(self):
        a=10
        b=123
        c=2.21

if __name__ == "__main__":
    # This code thinks that init code was already run from the
    # test/main.go source file
    db_config = DBConnectionInfo("test", "localhost", "adminadminadmin", "postgres")

    Py2SQL.db_connect(db_config)

    Py2SQL.db_save_class(TestClass)

    Py2SQL.db_disconnect()

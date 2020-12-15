import unittest

class Sample:
    foo: int
    bar: str

class SubSample(Sample):
    zoo: int

class Bar:
    done: bool

class TestSavingHierarchy(unittest.TestCase):
    def test_normal_usecase():
        # This code thinks that init code was already run from the
        # test/main.go source file
        db_config = DBConnectionInfo("test", "localhost", "adminadminadmin", "postgres")
        Py2SQL.db_connect(db_config)
        Py2SQL.save_hierarchy(SubSample)
        Py2SQL.db_disconnect()

if __name__ == "__main__":
    unittest.main()

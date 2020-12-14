from py2sql import *

class PyToSQL:
    @staticmethod
    def db_save_class(class_to_save):
        """Works
                Delete class_to_save if it exists
                Add table for class_to_save and columns for static types variables
        """
        data = Py2SQL.__dict__
#        var = Py2SQL.__connection

        cur = Py2SQL.GetConnection().cursor()

        class_name = str(class_to_save.__name__)

        if class_name.lower() in Py2SQL.db_tables():
            # delete from DB
            cur.execute("drop table " + class_name.lower())

        string_cmd = "create table " + class_name  # + \

        var_cmd = " ("
        var = class_to_save().__dict__.items()
        for (key, val) in class_to_save().__dict__.items():
            if type(val) == int:
                var_cmd += key + " bigint, "
            elif type(val) == float:
                var_cmd += key + " real, "
            elif type(val) == str:
                var_cmd += key + " text, "

        if var_cmd[-2:] == ', ':
            var_cmd = var_cmd[:-2]

        var_cmd += ");"

        cur.execute(string_cmd + var_cmd)

        Py2SQL.GetConnection().commit()
        cur.close()
        print(string_cmd + var_cmd)

    def db_delete_class(class_to_delete):
        cur = Py2SQL.__connection.cursor()

        class_name = str(class_to_delete.__name__)

        if class_name.lower() in Py2SQL.db_tables():
            # delete from DB
            cur.execute("drop table " + class_name.lower())

        Py2SQL.__connection.commit()
        cur.close()
        print("drop table " + class_name.lower())

    @staticmethod
    def db_save_object(object_to_save):
        cur = Py2SQL.__connection.cursor()

        data=object_to_save.__dict__.items()
        pass
from py2sql import *


class PyToSQL:
    @staticmethod
    def get_db_type(val):
        if type(val) == int:
            return "bigint"
        elif type(val) == float:
            return "real"
        elif type(val) == str:
            return "text"

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

        var_cmd = " (address bigint Primary key, "
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
        print(string_cmd.lower() + var_cmd.lower())

    @staticmethod
    def db_delete_class(class_to_delete):
        """
            delete class table from DB is it exists
            do nothing if it does not exits
        """

        cur = Py2SQL.GetConnection().cursor()

        class_name = str(class_to_delete.__name__)

        if class_name.lower() in Py2SQL.db_tables():
            # delete from DB
            cur.execute("drop table " + class_name.lower())

        Py2SQL.GetConnection().commit()
        cur.close()
        print("drop table " + class_name.lower())

    @staticmethod
    def db_save_object(object_to_save):
        """
                create a Table if it does not exist
                also add row with data to the Table
        """

        cur = Py2SQL.GetConnection().cursor()

        class_name = str(type(object_to_save).__name__)
        if not class_name.lower() in Py2SQL.db_tables():
            PyToSQL.db_save_class(type(object_to_save))

        base_cmd = "insert into " + class_name + " values ("
        id(object_to_save)
        var_cmd = str(id(object_to_save))+", "

        # get all vars from obj
        for key, val in object_to_save.__dict__.items():
            if PyToSQL.get_db_type(val) == "text":
                var_cmd += "'"
            var_cmd += str(val)
            if PyToSQL.get_db_type(val) == "text":
                var_cmd += "'"
            var_cmd += ", "

        if ', ' == var_cmd[-2:]:
            var_cmd = var_cmd[:-2]

        var_cmd += ");"

        cur.execute(base_cmd + var_cmd)

        Py2SQL.GetConnection().commit()
        cur.close()
        print(base_cmd.lower() + var_cmd.lower())

    @staticmethod
    def db_delete_object(object_to_delete):
        """
                        delete the row from class table if it exists
        """

        cur = Py2SQL.GetConnection().cursor()
        primary_key = str(id(object_to_delete))
        delete_cmd="delete from " + str(type(object_to_delete).__name__) +" where address = " + primary_key + " returning *;"
        cur.execute(delete_cmd)
        Py2SQL.GetConnection().commit()
        cur.close()
        print(delete_cmd)

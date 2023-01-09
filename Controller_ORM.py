import re

class db_controller():
    def __init__(self, model, view):
        self.__model = model
        self.__view = view
        self.main_process()

    def insert(self):
        table_names = self.__model.get_table_list()
        self.__view.table_menu(table_names)
        table = int(input())
        table = table_names[table - 1]
        columns = self.__model.get_column_names(table)
        values = []
        for i in range(len(columns)):
            print("Enter " + columns[i] + " value:")
            values.append(input())
        self.__model.insert_data(table, tuple(values))

    def delete(self):
        table_names = self.__model.get_table_list()
        self.__view.table_menu(table_names)
        table = int(input())
        table = table_names[table - 1]
        table_data = self.__model.get_table_data(table)
        self.__view.show_rows(table, table_data)
        prime_key = input('Enter primary key value (first value that occurs after row number): ')
        self.__model.delete_data(table, prime_key)

    def modify(self):
        table_names = self.__model.get_table_list()
        self.__view.table_menu(table_names)
        table = int(input())
        table = table_names[table - 1]
        table_data = self.__model.get_table_data(table)
        self.__view.show_rows(table, table_data)
        prime_key = input('Enter primary key value (first value that occurs after row number): ')
        columns = self.__model.get_column_names(table)
        values = []
        for i in range(len(columns)):
            print("Enter new " + columns[i] + " value:")
            values.append(input())
        self.__model.change_data(table, tuple(values), prime_key)

    def main_process(self):
        self.__view.starting_dialog()
        while 1:
            self.__view.main_menu()
            action = int(input())
            if action == 2:
                break
            elif action == 1:
                self.__view.operations_menu()
                operation = int(input())
                if operation == 1:
                    self.insert()
                elif operation == 2:
                    self.delete()
                elif operation == 3:
                    self.modify()
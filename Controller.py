import re

class db_controller():
    def __init__(self, model, view):
        self.__model = model
        self.__view = view
        self.main_process()

    def insert(self):
        table_names = self.__model.get_table_names()
        self.__view.table_menu(table_names)
        table = int(input())
        table = table_names[table - 1]
        table_data = self.__model.get_table_data(table)
        if re.match(r'.*_id', table_data[0][0]):
            table_data[0].pop(0)
        columns = table_data[0]
        values = []
        for i in range(len(columns)):
            print("Enter " + columns[i] + " value:")
            values.append(input())
        self.__model.insert_data(table, tuple(values), tuple(columns))

    def delete(self):
        table_names = self.__model.get_table_names()
        self.__view.table_menu(table_names)
        table = int(input())
        table = table_names[table - 1]
        table_data = self.__model.get_table_data(table)
        self.__view.show_rows(table_data[1])
        self.__model.delete_data(table, table_data[0][0], table_data[1][int(input('Choose row (enter number at the start of the row): '))-1][0])

    def modify(self):
        table_names = self.__model.get_table_names()
        self.__view.table_menu(table_names)
        table = int(input())
        table = table_names[table - 1]
        table_data = self.__model.get_table_data(table)
        self.__view.show_rows(table_data[1])
        attribute = table_data[0][0]
        row_number = table_data[1][int(input('Choose row (enter number at the start of the row): '))-1][0]
        if re.match(r'.*_id', table_data[0][0]):
            table_data[0].pop(0)
        values = []
        for i in range(len(table_data)):
            print("Enter new " + table_data[0][i] + " value:")
            values.append(input())
        self.__model.change_data(table, values, table_data[0], attribute, row_number)

    def rand_gen(self):
        table_names = self.__model.get_table_names()
        self.__view.table_menu(table_names)
        table = int(input())
        table = table_names[table - 1]
        self.__model.generate_data(table, int(input("Enter amount of rows to generate: ")))

    def find_sub_id_fee_tariff(self):
        sub_id_bottom = input("Enter bottom value of subscriber's id's range: ")
        sub_id_top = input("Enter top value of subscriber's id's range: ")
        fee_bottom = input("Enter bottom value of fee range: ")
        fee_top = input("Enter top value of fee range: ")
        tariff_pattern = input("Enter SQL LIKE pattern to match tariff name: ")
        result = self.__model.join_subscr_id_fee_tariff(sub_id_bottom, sub_id_top, fee_bottom, fee_top, tariff_pattern)
        self.__view.show_rows(result[1])
        print("Execution time: " + str(result[0]))

    def find_sub_id_sub1_start_time(self):
        sub_id_bottom = input("Enter bottom value of subscriber's id's range: ")
        sub_id_top = input("Enter top value of subscriber's id's range: ")
        sub1 = input("Enter SQL LIKE pattern to match first subscriber's phone number: ")
        start_time_bottom = input("Enter bottom value of calls starting times range: ")
        start_time_top = input("Enter top value of calls starting times range: ")
        result = self.__model.join_subscr_id_fee_tariff(sub_id_bottom, sub_id_top, sub1, start_time_bottom, start_time_top)
        self.__view.show_rows(result[1])
        print("Execution time: " + str(result[0]))

    def find_sub_id_sub1_end_time(self):
        sub_id_bottom = input("Enter bottom value of subscriber's id's range: ")
        sub_id_top = input("Enter top value of subscriber's id's range: ")
        sub1 = input("Enter SQL LIKE pattern to match first subscriber's phone number: ")
        end_time_bottom = input("Enter bottom value of calls ending times range: ")
        end_time_top = input("Enter top value of calls ending times range: ")
        result = self.__model.join_subscr_id_fee_tariff(sub_id_bottom, sub_id_top, sub1, end_time_bottom, end_time_top)
        self.__view.show_rows(result[1])
        print("Execution time: " + str(result[0]))

    def main_process(self):
        self.__view.starting_dialog()
        while 1:
            self.__view.main_menu()
            action = int(input())
            if action == 4:
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
            elif action == 2:
                self.__view.finding_requests_menu()
                request = int(input())
                if request == 1:
                    self.find_sub_id_fee_tariff()
                elif request == 2:
                    self.find_sub_id_sub1_start_time()
                elif request == 3:
                    self.find_sub_id_sub1_end_time()
            elif action == 3:
                self.rand_gen()
class db_view():
    def starting_dialog(self):
        print("""Welcome to phone node database application.
        To choose options from program menus, enter it's number which is written in front of it""")

    def main_menu(self):
        print("""MAIN MENU
        1. Data operations
        2. Finding requests
        3. Generate random data
        4. Quit""")

    def operations_menu(self):
        print("""OPERATIONS
        1. Insert data
        2. Delete data
        3. Modify data""")

    def finding_requests_menu(self):
        print("""REQUESTS
        1. Find rows from "tarification" and "subscriber" by subscriber's id, tariff and fee
        2. Find rows from "subscriber" and "call" by subscriber's id, first subscriber's phone number and call's start time
        3. Find rows from "subscriber" and "call" by subscriber's id, first subscriber's phone number and call's end time""")

    def table_menu(self, tables):
       print("""Choose table:""")
       for i in range(len(tables)):
           print(f"{i+1}.", tables[i])

    def show_rows(self, rows):
        number = 1
        for line in rows:
            string = f"{number}.\t"
            for elem in range(len(line)):
                string += str(line[elem]) + "\t"
            print(string)
            number += 1
class db_view():
    def starting_dialog(self):
        print("""Welcome to phone node database application.
        To choose options from program menus, enter it's number which is written in front of it""")

    def main_menu(self):
        print("""MAIN MENU
        1. Data operations
        2. Quit""")

    def operations_menu(self):
        print("""OPERATIONS
        1. Insert data
        2. Delete data
        3. Modify data""")

    def table_menu(self, tables):
       print("""Choose table:""")
       for i in range(len(tables)):
           print(f"{i+1}.", tables[i])

    def show_rows(self, table_name, rows):
        if table_name == 'tarification':
            i = 1
            for r in rows:
                print(str(i) + '. ' + str(r.subscr_id) + ' ' + str(r.fee) + ' ' + r.tariff)
                i = i + 1
        elif table_name == 'subscriber':
            i = 1
            for r in rows:
                print(str(i) + '. ' + r.number + ' ' + str(r.subscr_id) + ' ' + r.name)
                i = i + 1
        elif table_name == 'call':
            i = 1
            for r in rows:
                print(str(i) + '. ' + str(r.call_id) + ' ' + r.subscriber1 + ' ' + str(r.subscriber2) + ' ' + str(r.start_time) + ' ' + str(r.end_time))
                i = i + 1
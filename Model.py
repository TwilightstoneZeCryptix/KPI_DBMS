import psycopg2
from psycopg2 import sql
import time
import re

class db_model():

    def __init__(self, dbname, user_name, password, host):
        try:
            self.__context = psycopg2.connect(dbname=dbname, 
                                              user=user_name, 
                                              password=password, 
                                              host=host)
            self.__cursor = self.__context.cursor()
            self.__table_names = None
        except Exception as init_ex:
            print("Initialisation error: ", init_ex)
        return None

    def __del__(self):
        self.__cursor.close()
        self.__context.close()

    def get_table_names(self):
        if self.__table_names is None:
            self.__cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                """)
            self.__table_names = [table[0] for table in self.__cursor]
        return self.__table_names

    def get_column_types(self, table_name):
        self.__cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = %s
            ORDER BY table_schema, table_name
            """, (table_name,))
        return self.__cursor.fetchall()

    def get_column_names(self, table_name):
        self.__cursor.execute("""
            SELECT column_name FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = %s
            ORDER BY table_schema, table_name
            """, (table_name,))
        return [x[0] for x in self.__cursor.fetchall()]

    def get_foreign_key_info(self, table_name):
        self.__cursor.execute(""" 
           SELECT kcu.column_name, ccu.table_name AS 
                  foreign_table_name,
                  ccu.column_name AS foreign_column_name 
           FROM information_schema.table_constraints AS tc 
              JOIN information_schema.key_column_usage AS kcu
                 ON tc.constraint_name = kcu.constraint_name
                 AND tc.table_schema = kcu.table_schema
              JOIN information_schema.constraint_column_usage AS ccu
                 ON ccu.constraint_name = tc.constraint_name
                 AND ccu.table_schema = tc.table_schema
           WHERE tc.constraint_type = 'FOREIGN KEY' AND 
                          tc.table_name=%s;
           """, (table_name,))
        return self.__cursor.fetchall()

    def get_table_data(self, table_name):
        id_column = self.get_column_types(table_name)[0][0]
        cursor = self.__cursor
        try:
            cursor.execute(
                sql.SQL('SELECT * FROM {} ORDER BY {} ASC'
                      ).format(sql.Identifier(table_name), sql.SQL(id_column)))
        except Exception as e:
            return str(e)
        return ([col.name for col in cursor.description], cursor.fetchall())

    def test_is_referenced(self, table_name, column_name):
        for t in self.get_table_names():
            for k in self.get_foreign_key_info(t):
                if k[1] == table_name and k[2] == column_name:
                    return True
        return False

    def insert_data(self, table_name, values, columns):
        columns_line = '('
        values_line= '('
        for key in range(len(values)):
            if values[key]:
                columns_line += columns[key] + ','
                values_line += f"'{values[key]}'" + ','
        values_line = values_line[:-1] + ')'
        columns_line = columns_line[:-1] + ')'

        query = sql.SQL('INSERT INTO {table} {columns} VALUES {values}').format(
            table = sql.Identifier(table_name), 
            columns = sql.SQL(columns_line), 
            values = sql.SQL(values_line))

        try:
            self.__cursor.execute(query)
            self.__context.commit()
        except Exception as ins_ex:
            print(ins_ex)

    def change_data(self, table_name, new_values, columns, attr, cond):
        condition_line = f"{attr} = '{cond}'"
        new_values_line = ''
        for key in range(len(new_values)):
            if new_values[key]:
                new_values_line += f"{columns[key]} = '{new_values[key]}'" + ','
        new_values_line = new_values_line[:-1] + ''

        query = sql.SQL('UPDATE {table} SET {new_values} WHERE {condition}').format(
            table = sql.Identifier(table_name),
            new_values = sql.SQL(new_values_line), 
            condition = sql.SQL(condition_line))

        try:
            self.__cursor.execute(query)
            self.__context.commit()
        except Exception as chng_ex:
            print(chng_ex)

    def delete_data(self, table_name, attr, cond):
        condition_line = f"{attr} = {cond}"
        
        query = sql.SQL('DELETE FROM {table} WHERE {condition}').format(
            table = sql.Identifier(table_name), 
            condition = sql.SQL(condition_line))
        try:
            self.__cursor.execute(query)
            self.__context.commit()
        except Exception as del_ex:
            print(del_ex)

    def generate_data(self, table_name, count):
        types = self.get_column_types(table_name)
        fk_array = self.get_foreign_key_info(table_name)
        select_subquery = ""
        insert_query = "INSERT INTO " + table_name + " ("
        from_query = "generate_series(1," + str(count) + ") as ser"
        limit_query = " LIMIT " + str(count)
        pk = self.get_table_data(table_name)[0]
        pk = str(pk[0])
        for i in range(1 if re.match(r'.*_id', pk) else 0, len(types)):
            t = types[i]
            name = t[0]
            type = t[1]
            fk = [x for x in fk_array if x[0] == name]
            if fk:
                if self.test_is_referenced(table_name, str(fk[0][0])):
                    select_subquery += str(fk[0][2])
                    from_query += ", " + str(fk[0][1])
                else:
                    select_subquery += ('(SELECT {} FROM {} ORDER BY RANDOM(), ser LIMIT 1)'.format(fk[0][2], fk[0][1]))
            elif type == 'integer':
                select_subquery += 'trunc(random()*100)::INT'
            elif type == 'text':
                select_subquery += 'chr (trunc(65 + random()*52)::INT) || chr(trunc(65 + random()*52)::INT) || chr(trunc(65 + random()*52)::INT) || chr(trunc(65 + random()*52)::INT) || chr(trunc(65 + random()*52)::INT) || chr(trunc(65 + random()*52)::INT) || chr(trunc(65 + random()*52)::INT)'
            elif type == 'time without time zone':
                select_subquery += "time '00:00:00' + DATE_TRUNC('second',RANDOM() * time '24:00:00')"
            else:
                continue

            insert_query += name
            if i != len(types) - 1:
                select_subquery += ','
                insert_query += ','
            else:
                insert_query += ') '

        self.__cursor.execute(
            insert_query + "SELECT " + select_subquery + 
                    "FROM " + from_query + limit_query)
        self.__context.commit()

    def join_general(self, main_query, condition=""):
        new_cond = condition
        if condition:
            new_cond = "WHERE " + condition
        t1 = time.time()
        try:
            self.__cursor.execute(main_query.format(new_cond))
        except Exception as find_ex:
            print(find_ex)
        t2 = time.time()
        return ((t2 - t1) * 1000, self.__cursor.fetchall())

    def join_subscr_id_fee_tariff(self, sub_id_rng_start, sub_id_rng_end, fee_rng_start, fee_rng_end, tariff):
        sub_cond_1 = "s.subscr_id BETWEEN " + str(sub_id_rng_start) + " AND " + str(sub_id_rng_end)
        sub_cond_2 = "t.fee BETWEEN " + str(fee_rng_start) + " AND " + str(fee_rng_end)
        sub_cond_3 = "t.tariff LIKE " + "'" + str(tariff) + "'"
        condition =  sub_cond_1 + " AND " + sub_cond_2 + " AND " + sub_cond_3
        return self.join_general(
            """SELECT * FROM subscriber as s JOIN tarification as t ON s.subscr_id = t.subscr_id {} ORDER BY s.subscr_id ASC
            """, condition)

    def join_subscr_id_subscriber1_start_time(self, sub_id_rng_start, sub_id_rng_end, subscriber1, start_time_rng_start, start_time_rng_end):
        sub_cond_1 = "s.subscr_id BETWEEN " + str(sub_id_rng_start) + " AND " + str(sub_id_rng_end)
        sub_cond_2 = "c.subscriber1 LIKE " + "'" + str(subscriber1) + "'"
        sub_cond_3 = "c.start_time BETWEEN " + "'" + str(start_time_rng_start) + "'" + " AND " + "'" + str(start_time_rng_end) + "'"
        condition =  sub_cond_1 + " AND " + sub_cond_2 + " AND " + sub_cond_3
        return self.join_general(
            """SELECT * FROM subscriber as s JOIN call as c ON s.subscr_id = c.subscriber2 {} ORDER BY s.subscr_id ASC
            """, condition)

    def join_subscr_id_subscriber1_end_time(self, sub_id_rng_start, sub_id_rng_end, subscriber1, end_time_rng_start, end_time_rng_end):
        sub_cond_1 = "s.subscr_id BETWEEN " + str(sub_id_rng_start) + " AND " + str(sub_id_rng_end)
        sub_cond_2 = "c.subscriber1 LIKE " + "'" + str(subscriber1) + "'"
        sub_cond_3 = "c.end_time BETWEEN " + "'" + str(end_time_rng_start) + "'" + " AND " + "'" + str(end_time_rng_end) + "'"
        condition =  sub_cond_1 + " AND " + sub_cond_2 + " AND " + sub_cond_3
        return self.join_general(
            """SELECT * FROM subscriber as s JOIN call as c ON s.subscr_id = c.subscriber2 {} ORDER BY s.subscr_id ASC
            """, condition)








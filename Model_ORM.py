import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Tables import Tarification, Subscriber, Call
import time
import re

class db_model():
    def __init__(self, dbname, user_name, password, host):
        bd_acces_dir = 'postgresql' + '://' + user_name + ':' + password + '@' + host + ':5432/' + dbname
        try:
            self.__engine = create_engine(bd_acces_dir)
            self.__session = sessionmaker(bind = self.__engine)
        except Exception as init_ex:
            print("Initialisation error: ", init_ex)
        return None

    def __del__(self):
        pass

    def get_table_data(self, table_name):
        s = self.__session()
        if table_name == 'tarification':
            data = s.query(Tarification).all()
        elif table_name == 'subscriber':
            data = s.query(Subscriber).all()
        elif table_name == 'call':
            data = s.query(Call).all()
        s.close()
        return data

    def get_table_list(self):
        return ['tarification', 'subscriber', 'call']

    def get_column_names(self, table_name):
        if table_name == 'tarification':
            return ['fee', 'tariff']
        elif table_name == 'subscriber':
            return ['number', 'subscr_id', 'name']
        elif table_name == 'call':
            return ['subscriber1', 'subscriber2', 'start_time', 'end_time']

    def insert_data(self, table_name, values):
        s = self.__session()
        if table_name == 'tarification':
            data = Tarification(fee = values[0], tariff = values[1])
        elif table_name == 'subscriber':
            data = Subscriber(number = values[0], subscr_id = [1], name = values[2])
        elif table_name == 'call':
            data = Call(subscriber1 = values[0], subscriber2 = values[1], start_time = values[2], end_time = values[3])
        s.add(data)
        s.commit()
        s.close()

    def change_data(self, table_name, new_values,cond):
        s = self.__session()
        if table_name == 'tarification':
            data = s.query(Tarification).get(cond)
            data.fee = new_values[0]
            data.tariff = new_values[1]
        elif table_name == 'subscriber':
            data = s.query(Subscriber).get(cond)
            data.number = new_values[0]
            data.subscr_id = new_values[1]
            data.name = new_values[2]
        elif table_name == 'call':
            data = s.query(Call).get(cond)
            data.subscriber1 = new_values[0]
            data.subscriber2 = new_values[1]
            data.start_time = new_values[2]
            data.end_time = new_values[3]
        s.commit()
        s.close()

    def delete_data(self, table_name, cond):
        s = self.__session()
        if table_name == 'tarification':
            data = s.query(Tarification).get(cond)
        elif table_name == 'subscriber':
            data = s.query(Subscriber).get(cond)
        elif table_name == 'call':
            data = s.query(Call).get(cond)
        s.delete(data)
        s.commit()
        s.close()








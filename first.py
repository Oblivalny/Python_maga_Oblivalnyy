import pandas as pd
from datetime import datetime
from db_mysql import *

class Good(object):
    prise = None
    name = None
    size = None
    manufacturer = None

    def __init__(self, name, prise, size, manufacturer):

        self.name = name
        self.prise = prise
        self.size = size
        self.manufacturer = manufacturer


class Warehouse(object):

    dict_count_goods = {}
    list_goods = []
    path_to_warehouse_save = ''

    def __init__(self, path_to_warehouse_save):
        self.dict_count_goods = {}
        self.list_goods = []
        self.path_to_warehouse_save = path_to_warehouse_save
        # self.read_csv()

    def add_new_good(self, good):
        new_good = Good_tb(good.name, good.prise, good.manufacturer, good.size)
        session.add(new_good)
        session.commit()

    def add_good(self, name, count):
        session.query(Good_tb).filter(Good_tb.name == name).update({Good_tb.count: Good_tb.count+count}, synchronize_session=False)
        session.commit()

    def del_good(self, name, count):
        old_val = session.query(Good_tb).filter(Good_tb.name == name).first().count
        if old_val - count < 0:
            print(f'''На складе нет такого количества товаров. В наличии всего {old_val}''')
        else:
            self.add_good(name, count*-1)

    def get_count_goods(self):
        for row in session.query(Good_tb).all():
            print(row.name, row.count)

    def get_stat_size(self):
        for row in session.query(Good_tb.size, func.count(Good_tb.size)).group_by(Good_tb.size).all():
            print(row)

    def get_stat_manufacturer(self):
        for row in session.query(Good_tb.manufacturer, func.count(Good_tb.manufacturer)).group_by(Good_tb.manufacturer).all():
            print(row)

    def read_csv(self, path=''):
        if path == '':
            path = self.path_to_warehouse_save

        df = pd.read_csv(path)
        for i in range(df.shape[0]):
            if session.query(Good_tb).filter_by(name=df.iloc[i]['name']).first() is None:
                self.add_good(df.iloc[i]['name'], df.iloc[i]['count'])
            else:
                goods = Good(df.iloc[i]['name'], df.iloc[i]['prise'], df.iloc[i]['size'], df.iloc[i]['manufacturer'])
                self.add_new_good(goods)
                self.add_good(df.iloc[i]['name'], df.iloc[i]['count'])

    def to_csv(self, path=''):

        if path == '':
            path = self.path_to_warehouse_save

        dict_values = {'name':[], 'prise':[], 'size':[], 'manufacturer':[], 'count':[]}
        for good in session.query(Good_tb).all():
            dict_values['name'].append(good.name)
            dict_values['prise'].append(good.prise)
            dict_values['size'].append(good.size)
            dict_values['manufacturer'].append(good.manufacturer)
            dict_values['count'].append(good.count)

        df = pd.DataFrame(dict_values)
        df.to_csv(f'''{path}_{str(datetime.now().date())}''')


class Command(object):

    list_command = [
        'add_good',
        'look',
        'read_csv',
        'to_csv',
        'del',
        'stat_size',
        'stat_manufacturer',
        'help',
        'stop',
    ]

    def execute_command(self, run_command, warehouse):

        if run_command == 'add_good':
            print('Введите  name')
            name = input()
            print('Введите  count')
            count = int(input())

            if session.query(Good_tb).filter_by(name=name).first() is None:
                print('Введите  prise')
                prise = int(input())
                print('Введите  size')
                size = input()
                print('Введите  manufacturer')
                manufacturer = input()

                good = Good(name, prise, size, manufacturer)
                warehouse.add_new_good(good)

            warehouse.add_good(name, count)
            print('------------------')

        elif run_command == 'look':
            print(warehouse.get_count_goods())
            print('------------------')

        elif run_command == 'read_csv':
            print('Введите  path')
            path = input()
            print(warehouse.read_csv(path))
            print('------------------')

        elif run_command == 'to_csv':
            print('Введите  path')
            path = input()
            print(warehouse.to_csv(path))
            print('------------------')

        elif run_command == 'del':
            print('Введите  name')
            name = input()
            print('Введите  count')
            count = int(input())

            warehouse.del_good(name, count)
            print('------------------')

        elif run_command == 'stat_size':
            print(warehouse.get_stat_size())
            print('------------------')

        elif run_command == 'stat_manufacturer':
            print(warehouse.get_stat_manufacturer())
            print('------------------')

        elif run_command == 'help':
            print(self.list_command)
            print('------------------')

        elif run_command == 'stop':

            warehouse.to_csv()
            print('------------------')


# ====================================================


df = pd.DataFrame(
    {
        'name': ['Шерты', 'GG', 'Гамбургер'],
        'prise': [100, 1, 799],
        'size': ['M', 0, 'Big'],
        'manufacturer': ['Китай', 'Колывандия', 'USA'],
        'count': [10, 5, 2]
})

df.to_csv('goods_file.csv', index=False)


command = Command()
warehouse = Warehouse('goods_file.csv')

engine = connect('root', 'root', echo=False)
session = create_session(engine)
migration(engine)

print('comand:\n ', command.list_command)
work = True

while work:

    run_command = input()
    command.execute_command(run_command, warehouse)

    if run_command == 'stop':
        work = False






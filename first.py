import pandas as pd

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

    def __init__(self):
        self.dict_count_goods = {}
        self.list_goods = []

    def add_new_good(self, good):
        if good in self.list_goods:
            print('Этот товар уже существует')
        else:
            self.list_goods.append(good)
            self.dict_count_goods[good.name] = 0

    def add_good(self, name, count):
        if name in self.dict_count_goods:
            self.dict_count_goods[name] += count
        else:
            self.dict_count_goods[name] = count

    def del_good(self, name, count):

        if name in self.dict_count_goods:
            if self.dict_count_goods[name] - count >= 0:
                self.dict_count_goods[name] -= count
            else:
                self.dict_count_goods[name] = 0

        else:
            print('Этого товара не существует')

    def get_count_goods(self):
        return self.dict_count_goods

    def get_stat_size(self):
        dict_size = {}
        for good in self.list_goods:
            if good.size in dict_size:
                dict_size[good.size] += self.dict_count_goods[good.name]
            else:
                dict_size[good.size] = self.dict_count_goods[good.name]

        return dict_size

    def get_stat_manufacturer(self):
        dict_manufacturer = {}
        for good in self.list_goods:
            if good.size in dict_manufacturer:
                dict_manufacturer[good.manufacturer] += self.dict_count_goods[good.name]
            else:
                dict_manufacturer[good.manufacturer] = self.dict_count_goods[good.name]

        return dict_manufacturer


    def read_csv(self, path):
        df = pd.read_csv(path)
        for i in range(df.shape[0]):
            if df.iloc[i]['name'] in self.dict_count_goods:
                self.add_good(df.iloc[i]['name'], df.iloc[i]['count'])
            else:
                goods = Good(df.iloc[i]['name'], df.iloc[i]['prise'], df.iloc[i]['size'], df.iloc[i]['manufacturer'])
                self.add_new_good(goods)
                self.add_good(df.iloc[i]['name'], df.iloc[i]['count'])



class Command(object):

    list_command = [
        'add_good',
        'look',
        'read_csv',
        'del',
        'stat_size',
        'stat_manufacturer',
        'help',
    ]

    def execute_command(self, run_command, warehouse):

        if run_command == 'add_good':
            print('Введите  name')
            name = input()
            print('Введите  count')
            count = int(input())

            if not name in warehouse.list_goods:
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
warehouse = Warehouse()
print('comand:\n ', command.list_command)

while True:
    run_command = input()
    command.execute_command(run_command, warehouse)






import pandas as pd
from datetime import datetime
from db_mysql import *




class Product(object):
    sku = None
    prise = None
    name = None
    brand = None
    quantity = None

    def __init__(self, console=False):
        if console:
            print('Введите  sku')
            self.sku = int(input())
            print('Введите  prise')
            self.prise = int(input())
            print('Введите  brand')
            self.brand = input()
            print('Введите  quantity')
            self.quantity = int(input())

    def db_add_product(self, session):

        if session.query(Product_tb).filter_by(sku=self.sku).first() is None:
            new_good = Product_tb(sku=self.sku,
                                  name=self.name,
                                  prise=self.prise,
                                  brand=self.brand,
                                  quantity=self.quantity)
            session.add(new_good)
            session.commit()

        else:
            session.query(Product_tb).filter(
                Product_tb.sku == self.sku).update(
                {Product_tb.count: Product_tb.quantity+self.quantity}, synchronize_session=False)
            session.commit()


class TshirtProduct(Product):
    size = None
    color = None

    def __init__(self, console=False):
        super().__init__(console)
        if console:
            print('Введите  size')
            self.size = str(input())
            print('Введите  color')
            self.color = str(input())

    def db_add_product(self, session):
        super().db_add_product(session)
        if session.query(Tshirt_product_tb).filter_by(sku=self.sku).first() is None:
            new_good = Tshirt_product_tb(sku=self.sku, size=self.size, color=self.color)
            session.add(new_good)
            session.commit()


class FoodProduct(Product):
    shelf_life = None

    def __init__(self, console=False):
        super().__init__(console)
        if console:
            print('Введите  shelf_life  example: "01-01-2020" ')
            self.shelf_life = datetime.strptime(str(input()), '%d-%m-%Y')

    def db_add_product(self, session):
        super().db_add_product(session)
        if session.query(Food_product_tb).filter_by(sku=self.sku).first() is None:
            new_good = Food_product_tb(sku=self.sku, shelf_life=self.shelf_life)
            session.add(new_good)
            session.commit()


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
        new_good = Product_tb(good.name, good.prise, good.brand, good.size)
        session.add(new_good)
        session.commit()

    def add_good(self, name, count):
        session.query(Product_tb).filter(Product_tb.name == name).update({Product_tb.count: Product_tb.count+count}, synchronize_session=False)
        session.commit()

    def del_good(self, name, count):
        old_val = session.query(Product_tb).filter(Product_tb.name == name).first().count
        if old_val - count < 0:
            print(f'''На складе нет такого количества товаров. В наличии всего {old_val}''')
        else:
            self.add_good(name, count*-1)

    def get_count_goods(self):
        for row in session.query(Product_tb).all():
            print(row.name, row.count)

    def get_stat_size(self):
        for row in session.query(Product_tb.size, func.count(Product_tb.size)).group_by(Product_tb.size).all():
            print(row)

    def get_stat_brand(self):
        for row in session.query(Product_tb.brand, func.count(Product_tb.brand)).group_by(Product_tb.brand).all():
            print(row)

    def read_csv(self, path=''):
        if path == '':
            path = self.path_to_warehouse_save

        df = pd.read_csv(path)
        for i in range(df.shape[0]):
            if session.query(Product_tb).filter_by(name=df.iloc[i]['name']).first() is None:
                self.add_good(df.iloc[i]['name'], df.iloc[i]['count'])
            else:
                goods = Good(df.iloc[i]['name'], df.iloc[i]['prise'], df.iloc[i]['size'], df.iloc[i]['brand'])
                self.add_new_good(goods)
                self.add_good(df.iloc[i]['name'], df.iloc[i]['count'])

    def to_csv(self, path=''):

        if path == '':
            path = self.path_to_warehouse_save

        dict_values = {'name':[], 'prise':[], 'size':[], 'brand':[], 'count':[]}
        for good in session.query(Product_tb).all():
            dict_values['name'].append(good.name)
            dict_values['prise'].append(good.prise)
            dict_values['size'].append(good.size)
            dict_values['brand'].append(good.brand)
            dict_values['count'].append(good.count)

        df = pd.DataFrame(dict_values)
        df.to_csv(f'''{path}_{str(datetime.now().date())}''')


class Command(object):
    warehouse = Warehouse('goods_file.csv')

    engine = None
    session = None

    list_product = ['Tshirt', 'Food']

    list_command = [
        'add_good',
        'look',
        'read_csv',
        'to_csv',
        'del',
        'stat_size',
        'stat_brand',
        'help',
        'stop',
    ]

    def __init__(self, username='root', pw='root', echo=False, migration_db=True):
        self.engine = connect(username, pw, echo=echo)
        self.session = create_session(self.engine)
        if migration_db:
            migration(self.engine)


    def execute_command(self, run_command, warehouse):

        if run_command == 'add_good':
            print(f'''Выберите тип товара: {self.list_product}''')
            product_type = input()

            if product_type in self.list_product:

                #------tyt----Ploho-------
                if product_type == 'Tshirt':
                    product = TshirtProduct(console=True)

                elif product_type == 'Food':
                    product = FoodProduct(console=True)

                product.db_add_product(session=self.session)

            else:
                print('Нет такой категории товара')

            print('------------------')

        # elif run_command == 'look':
        #     print(warehouse.get_count_goods())
        #     print('------------------')


        #
        # elif run_command == 'read_csv':
        #     print('Введите  path')
        #     path = input()
        #     print(warehouse.read_csv(path))
        #     print('------------------')
        #
        # elif run_command == 'to_csv':
        #     print('Введите  path')
        #     path = input()
        #     print(warehouse.to_csv(path))
        #     print('------------------')
        #
        # elif run_command == 'del':
        #     print('Введите  name')
        #     name = input()
        #     print('Введите  count')
        #     count = int(input())
        #
        #     warehouse.del_good(name, count)
        #     print('------------------')
        #
        # elif run_command == 'stat_size':
        #     print(warehouse.get_stat_size())
        #     print('------------------')
        #
        # elif run_command == 'stat_brand':
        #     print(warehouse.get_stat_brand())
        #     print('------------------')
        #
        # elif run_command == 'help':
        #     print(self.list_command)
        #     print('------------------')
        #
        # elif run_command == 'stop':
        #
        #     warehouse.to_csv()
        #     print('------------------')


# ====================================================


df = pd.DataFrame(
    {
        'name': ['Шерты', 'GG', 'Гамбургер'],
        'prise': [100, 1, 799],
        'size': ['M', 0, 'Big'],
        'brand': ['Китай', 'Колывандия', 'USA'],
        'count': [10, 5, 2]
})

df.to_csv('goods_file.csv', index=False)


command = Command('root', 'root')


print('comand:\n ', command.list_command)
work = True

while work:

    run_command = input()
    command.execute_command(run_command, warehouse)

    if run_command == 'stop':
        work = False





